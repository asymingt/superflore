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

import os
from rosdistro.dependency_walker import DependencyWalker
from rosdistro.rosdistro import RosPackage
from rosinstall_generator.distro import get_package_names
from superflore.exceptions import UnresolvedDependency
from superflore.PackageMetadata import PackageMetadata
from superflore.utils import err
from superflore.utils import get_distros
from superflore.utils import get_pkg_version
from superflore.utils import make_dir
from superflore.utils import ok
from superflore.utils import retry_on_exception
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

def regenerate_pkg(overlay, pkg, distro, preserve_existing=False):
    version = get_pkg_version(distro, pkg)
    pkg_names = get_package_names(distro)[0]
    
    if pkg not in pkg_names:
        raise RuntimeError("Unknown package '%s'" % (pkg))

    # Directory/File structure: repo_dir/ros-<distro>/<pkg>/MODULE.bazel
    pkg_dir = '{0}/ros-{1}/{2}'.format(overlay.repo.repo_dir, distro.name, pkg)
    module_file_path = os.path.join(pkg_dir, 'MODULE.bazel')
    
    if preserve_existing and os.path.isfile(module_file_path):
        ok("MODULE file for package '%s' up to date, skipping..." % pkg)
        return None, [], None

    make_dir(pkg_dir)

    try:
        current = BazelPackage(distro, pkg)
    except Exception as e:
        err('Failed to generate MODULE for package {}!'.format(pkg))
        raise e
        
    try:
        module_text = current.module_text()
    except UnresolvedDependency:
        err("Failed to resolve dependencies for package {}!".format(pkg))
        return None, [], None
    except KeyError as ke:
        err("Failed to parse data for package {}!".format(pkg))
        raise ke

    try:
        with open(module_file_path, "w") as f:
            f.write(module_text)
    except Exception as e:
        err("Failed to write MODULE file to disk!")
        raise e
        
    success_msg = 'Successfully generated MODULE for package'
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
