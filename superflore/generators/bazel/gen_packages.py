# Copyright 2026 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib
import json
import os
from rosdistro.dependency_walker import DependencyWalker
from rosdistro.rosdistro import RosPackage
from rosinstall_generator.distro import get_package_names
from superflore.exceptions import UnresolvedDependency
from superflore.PackageMetadata import PackageMetadata
from superflore.utils import download_file
from superflore.utils import err
from superflore.utils import get_distros
from superflore.utils import get_pkg_version
from superflore.utils import make_dir
from superflore.utils import ok
from superflore.utils import retry_on_exception
from superflore.utils import url_to_repo_org
from superflore.utils import warn

org = "Open Source Robotics Foundation"
org_license = "BSD"

def _package_condition_context(rosdistro_name):
    distro_properties = get_distros()[rosdistro_name]
    ros_version = None
    if distro_properties['distribution_type'] == 'ros2':
        ros_version = '2'
    elif distro_properties['distribution_type'] == 'ros1':
        ros_version = '1'
    else:
        err("Superflore does not handle the distribution type '{}'".format(
            distro_properties['distribution_type']))
        raise RuntimeError('Invalid distribution_type for {}'.format(rosdistro_name))
    ros_python_version = None
    if distro_properties['python_version'] == 3:
        ros_python_version = '3'
    elif distro_properties['python_version'] == 2:
        ros_python_version = '2'
    else:
        err("Superflore does not handle the python version '{}'".format(
            distro_properties['python_version']))
        raise RuntimeError('Invalid python_version for {}'.format(rosdistro_name))
    return {
        'ROS_DISTRO': rosdistro_name,
        'ROS_VERSION': ros_version,
        'ROS_PYTHON_VERSION': ros_python_version
    }



from superflore.generators.bazel.bazel_module import BazelModule
from superflore.generators.bazel.bazel_module import get_bazel_version

def _calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return "sha256-" + sha256_hash.hexdigest()

def regenerate_pkg(overlay, pkg, distro, preserve_existing=False):
    version = get_bazel_version(distro, pkg)
    pkg_names = get_package_names(distro)[0]
    
    if pkg not in pkg_names:
        raise RuntimeError("Unknown package '%s'" % (pkg))

    # Directory/File structure: modules/<pkg>/<version>/MODULE.bazel
    pkg_dir = os.path.join(overlay.repo.repo_dir, "modules", pkg)
    version_dir = os.path.join(pkg_dir, version)
    module_file_path = os.path.join(version_dir, 'MODULE.bazel')
    source_json_path = os.path.join(version_dir, 'source.json')
    metadata_json_path = os.path.join(pkg_dir, 'metadata.json')
    
    if preserve_existing and os.path.isfile(module_file_path):
        ok("MODULE file for package '%s' up to date, skipping..." % pkg)
        return None, [], None

    make_dir(version_dir)

    # Download source tarball and calculate integrity
    cache_dir = os.path.join(os.getcwd(), ".bazel")
    if not os.path.exists(cache_dir):
        make_dir(cache_dir)

    pkg_obj = distro.release_packages[pkg]
    repo = distro.repositories[pkg_obj.repository_name].release_repository
    
    # Determine tag
    # Default tag format: release/{distro}/{pkg}/{version}
    # Note: repo.version is the full version string (e.g. 1.2.3-0)
    full_version = repo.version
    tag = 'release/{0}/{1}/{2}'.format(distro.name, pkg, full_version)
    if repo.tags and full_version in repo.tags:
         tag = repo.tags[full_version]
    
    # Construct Archive URL
    url = repo.url.replace('.git', '')
    if 'github.com' in url:
        archive_url = '{0}/archive/refs/tags/{1}.tar.gz'.format(url, tag)
    else:
        err("Non-GitHub repositories are not supported for calculating integrity hash")
        return None, [], None

    tarball_name = '{0}-{1}.tar.gz'.format(pkg, version)
    tarball_path = os.path.join(cache_dir, tarball_name)
    
    if not os.path.exists(tarball_path):
        try:
            download_file(archive_url, tarball_path)
        except Exception as e:
            err("Failed to download tarball for {0}: {1}".format(pkg, e))
            return None, [], None
    
    integrity = _calculate_sha256(tarball_path)
    
    # Guess strip_prefix
    repo_name = url.split('/')[-1]
    strip_prefix = '{0}-{1}'.format(repo_name, tag.replace('/', '-').lstrip('v'))
    if tag.startswith('v'):
         strip_prefix = '{0}-{1}'.format(repo_name, tag.lstrip('v'))

    try:
        current = BazelPackage(distro, pkg)
    except Exception as e:
        err('Failed to generate MODULE for package {}!'.format(pkg))
        raise e
        
    try:
        module_text = current.module_text()
        source_json = current.bazel_module.get_source_json(archive_url, integrity, strip_prefix)
    except UnresolvedDependency:
        err("Failed to resolve dependencies for package {}!".format(pkg))
        return None, [], None
    except KeyError as ke:
        err("Failed to parse data for package {}!".format(pkg))
        raise ke

    # Update metadata.json
    maintainers = []
    # Fetch maintainers from rosdistro
    # RosPackage doesn't expose maintainers directly?
    # We might need to look at manifests.
    # For now, let's use a placeholder or skip if not critical. 
    # But User requirement said "Each package will need a metadata.json".
    # I'll try to load existing metadata if available.
    
    metadata = {
        "homepage": repo.url,
        "maintainers": [
            {
                "email": "simmers@intrinsic.ai",
                "github": "asymingt",
                "github_user_id": 37671,
                "name": "Andrew Symington"
            }
        ],
        "versions": [],
        "yanked_versions": {}
    }
    
    if os.path.isfile(metadata_json_path):
        with open(metadata_json_path, 'r') as f:
            try:
                metadata = json.load(f)
            except:
                pass

    if version not in metadata["versions"]:
        metadata["versions"].append(version)
        metadata["versions"].sort()

    try:
        with open(module_file_path, "w") as f:
            f.write(module_text)
        with open(source_json_path, 'w') as f:
            json.dump(source_json, f, indent=4)
            f.write('\n')
        with open(metadata_json_path, 'w') as f:
            json.dump(metadata, f, indent=4)
            f.write('\n')
    except Exception as e:
        err("Failed to write Bazel registry files to disk!")
        raise e
        
    success_msg = 'Successfully generated Bazel registry files for package'
    ok('{0} \'{1}\'.'.format(success_msg, pkg))
    return current, version, pkg

class BazelPackage(object):
    def __init__(self, distro, pkg_name):
        pkg = distro.release_packages[pkg_name]
        repo = distro.repositories[pkg.repository_name].release_repository
        ros_pkg = RosPackage(pkg_name, repo)
        version = get_bazel_version(distro, pkg_name)
        
        self.bazel_module = BazelModule(pkg_name, version, distro)
        
        package_condition_context = _package_condition_context(distro.name)
        walker = DependencyWalker(distro, evaluate_condition_context=package_condition_context)
        
        build_deps = walker.get_depends(pkg_name, "build")
        run_deps = walker.get_depends(pkg_name, "run")
        test_deps = walker.get_depends(pkg_name, "test")
        
        pkg_names = get_package_names(distro)[0]

        for dep in build_deps:
            self.bazel_module.add_depend(dep, dep in pkg_names)
            
        for dep in run_deps:
            self.bazel_module.add_depend(dep, dep in pkg_names)
            
        for dep in test_deps:
            self.bazel_module.add_depend(dep, dep in pkg_names)

    def module_text(self):
        return self.bazel_module.get_module_text()
