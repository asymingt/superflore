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
import re
import sys
import json
import tempfile
import subprocess
import urllib.request
from superflore.utils import download_file
from superflore.generators.bazel.gen_packages import _calculate_sha256

from rosinstall_generator.distro import get_distro
from rosinstall_generator.distro import get_package_names
from superflore.exceptions import NoGitHubAuthToken
from superflore.generate_installers import generate_installers
from superflore.generators.bazel.bazel_module import (
    DEFAULT_DEPS,
    DEP_NAME_OVERRIDE,
    DEP_IGNORES,
    get_bazel_version,
    get_copyright_header,
)
from superflore.generators.bazel.gen_packages import regenerate_pkg
from superflore.generators.bazel.overlay_instance import BazelOverlay
from superflore.parser import get_parser
from superflore.repo_instance import RepoInstance
from superflore.TempfileManager import TempfileManager
from superflore.utils import clean_up
from superflore.utils import err
from superflore.utils import file_pr
from superflore.utils import gen_delta_msg
from superflore.utils import gen_missing_deps_msg
from superflore.utils import get_distros_by_status
from superflore.utils import info
from superflore.utils import load_pr
from superflore.utils import make_dir
from superflore.utils import ok
from superflore.utils import save_pr
from superflore.utils import url_to_repo_org
from superflore.utils import warn

def main():
    overlay = None
    preserve_existing = True
    parser = get_parser('Deploy ROS packages into a Bazel workspace', require_rosdistro=True, require_ros_tag_date=True)
    args = parser.parse_args(sys.argv[1:])
    ########################################################################################
    # TODO(asymingt) - this in principle should work correctly. However, there is a bug with
    # release tags, and how they incorrectly use a distribution cache.
    # See: https://github.com/asymingt/rosdistro/blob/rolling-bazel/.github/workflows/preserve_cache.yaml
    url = 'https://github.com/asymingt/rosdistro/releases/download/{0}/{1}/index-v4.yaml'.format(
        args.ros_distro,
        args.ros_tag_date
    )
    info('Using rosdistro index: {0}'.format(url))
    os.environ['ROSDISTRO_INDEX_URL'] = url
    ########################################################################################
    pr_comment = args.pr_comment
    skip_keys = args.skip_keys or []
    skip_keys.extend(DEP_NAME_OVERRIDE.keys())
    skip_keys.extend(DEP_IGNORES)
    selected_targets = None
    if not args.dry_run:
        if 'SUPERFLORE_GITHUB_TOKEN' not in os.environ:
            raise NoGitHubAuthToken()
    if args.pr_only:
        if args.dry_run:
            parser.error('Invalid args! cannot dry-run and file PR')
        if not args.output_repository_path:
            parser.error('Invalid args! no repository specified')
        try:
            prev_overlay = RepoInstance(args.output_repository_path, False)
            msg, title = load_pr()
            prev_overlay.pull_request(msg, title=title)
            clean_up()
            sys.exit(0)
        except Exception as e:
            err('Failed to file PR!')
            err('reason: {0}'.format(e))
            sys.exit(1)
    elif args.all:
        warn('"All" mode detected... This may take a while!')
        preserve_existing = False
    elif args.ros_distro:
        warn('"{0}" distro detected...'.format(args.ros_distro))
        selected_targets = [args.ros_distro]
        preserve_existing = False
    elif args.only:
        parser.error('Invalid args! --only requires specifying --ros-distro')
    if not selected_targets:
        selected_targets = get_distros_by_status('active')
    repo_org = 'ros'
    repo_name = 'ros-bazel-overlay'
    if args.upstream_repo:
        repo_org, repo_name = url_to_repo_org(args.upstream_repo)
    with TempfileManager(args.output_repository_path) as _repo:
        if not args.output_repository_path:
            # give our group write permissions to the temp dir
            os.chmod(_repo, 17407)
        # clone if args.output_repository_path is None
        overlay = BazelOverlay(
            _repo,
            not args.output_repository_path,
            org=repo_org,
            repo=repo_name,
            from_branch=args.upstream_branch,
            new_branch=(not args.no_branch),
        )
        if not preserve_existing and not args.only:
            pr_comment = pr_comment or (
                'Superflore bazel generator began regeneration of all'
                ' packages from ROS distro %s from ROS-Bazel-Overlay commit %s.' % (
                    selected_targets,
                    overlay.repo.get_last_hash()
                )
            )
        elif not args.only:
            pr_comment = pr_comment or (
                'Superflore bazel generator ran update from ROS-Bazel-Overlay ' +
                'commit %s.' % (overlay.repo.get_last_hash())
            )
        # generate installers
        total_installers = dict()
        total_broken = set()
        total_changes = dict()
        if args.only:
            pr_comment = pr_comment or (
                'Superflore bazel generator began regeneration of ' +
                'package(s) %s from commit %s.' % (
                    args.only,
                    overlay.repo.get_last_hash()
                )
            )
            missing_depends = set()
            to_commit = set()
            will_file_pr = False
            for pkg in args.only:
                if pkg in skip_keys:
                    warn("Package '%s' is in skip-keys list, skipping..."
                         % pkg)
                    continue
                info("Regenerating package '%s'..." % pkg)
                try:
                    d_obj = get_distro(args.ros_distro)
                    d_obj.ros_tag_date = args.ros_tag_date
                    current, current_info, pkg = regenerate_pkg(
                        overlay,
                        pkg,
                        d_obj,
                        preserve_existing
                    )
                    if not current:
                        # process missing deps if any, current_info might be list of deps
                        if isinstance(current_info, list):
                             for dep in current_info:
                                 missing_depends.add(dep)
                except KeyError:
                    err("No package to satisfy key '%s'" % pkg)
                    continue
                if current:
                    to_commit.add(pkg)
                    will_file_pr = True
            # if no packages succeeded, exit with error
            if not will_file_pr:
                err("No packages generated successfully, exiting.")
                sys.exit(1)
            # Commit changes and file pull request
            if args.no_commit:
                info('Skipping commit (--no-commit), changes left unstaged')
            else:
                overlay.commit_changes(args.ros_distro)
            delta = "Regenerated: '%s'\n" % args.only
            if args.dry_run:
                save_pr(
                    overlay,
                    delta,
                    missing_deps=gen_missing_deps_msg(missing_depends),
                    comment=pr_comment
                )
                sys.exit(0)
            file_pr(
                overlay,
                delta,
                gen_missing_deps_msg(missing_depends),
                pr_comment
            )
            ok('Successfully synchronized repositories!')
            sys.exit(0)

        for distro in selected_targets:
            distro_obj = get_distro(distro)
            distro_obj.ros_tag_date = args.ros_tag_date
            distro_installers, distro_broken, distro_changes =\
                generate_installers(
                    distro_obj,
                    overlay=overlay,
                    gen_pkg_func=regenerate_pkg,
                    preserve_existing=preserve_existing,
                    skip_keys=skip_keys,
                )
            for key in distro_broken.keys():
                for pkg in distro_broken[key]:
                    total_broken.add(pkg)

            total_changes[distro] = distro_changes
            total_installers[distro] = distro_installers

            # Generate rosdistro module
            rosdistro_module_name = "rosdistro"
            rosdistro_version = "{0}.{1}".format(distro, args.ros_tag_date)
            rosdistro_pkg_dir = os.path.join(overlay.repo.repo_dir, "modules", rosdistro_module_name)
            rosdistro_version_dir = os.path.join(rosdistro_pkg_dir, rosdistro_version)
            make_dir(rosdistro_version_dir)

            rosdistro_url = "https://github.com/ros/rosdistro/archive/refs/tags/{0}/{1}.tar.gz".format(distro, args.ros_tag_date)
            
            with tempfile.NamedTemporaryFile(suffix=".tar.gz") as tmpf:
                download_file(rosdistro_url, tmpf.name)
                rosdistro_integrity = _calculate_sha256(tmpf.name)
            
            rosdistro_strip_prefix = "rosdistro-{0}-{1}".format(distro, args.ros_tag_date)
            rosdistro_source_json = {
                "url": rosdistro_url,
                "integrity": rosdistro_integrity,
                "strip_prefix": rosdistro_strip_prefix
            }
            with open(os.path.join(rosdistro_version_dir, "source.json"), "w") as f:
                json.dump(rosdistro_source_json, f, indent=4)
                f.write("\n")
                
            rosdistro_metadata_path = os.path.join(rosdistro_pkg_dir, "metadata.json")
            rosdistro_metadata = {"versions": []}
            if os.path.exists(rosdistro_metadata_path):
                with open(rosdistro_metadata_path, 'r') as f:
                    rosdistro_metadata = json.load(f)
            if rosdistro_version not in rosdistro_metadata["versions"]:
                rosdistro_metadata["versions"].append(rosdistro_version)
                rosdistro_metadata["versions"].sort()
            with open(rosdistro_metadata_path, "w") as f:
                json.dump(rosdistro_metadata, f, indent=4)
                f.write("\n")
                
            rosdistro_module_content = get_copyright_header() + "module(\n"
            rosdistro_module_content += '    name = "{0}",\n'.format(rosdistro_module_name)
            rosdistro_module_content += '    version = "{0}",\n'.format(rosdistro_version)
            rosdistro_module_content += ")\n"
            with open(os.path.join(rosdistro_version_dir, "MODULE.bazel"), "w") as f:
                f.write(rosdistro_module_content)

            # Generate ros module
            ros_module_name = "ros"
            ros_version = "{0}.{1}".format(distro, args.ros_tag_date)
            ros_pkg_dir = os.path.join(overlay.repo.repo_dir, "modules", ros_module_name)
            ros_version_dir = os.path.join(ros_pkg_dir, ros_version)
            make_dir(ros_version_dir)
            
            commit = subprocess.check_output(['git', 'ls-remote', 'https://github.com/ros2/ros2.git', 'refs/heads/{0}'.format(distro)]).decode('utf-8').split()[0]
            ros_url = "https://github.com/ros2/ros2/archive/{0}.zip".format(commit)
            
            with tempfile.NamedTemporaryFile(suffix=".zip") as tmpf:
                download_file(ros_url, tmpf.name)
                ros_integrity = _calculate_sha256(tmpf.name)
                
            ros_source_json = {
                "url": ros_url,
                "integrity": ros_integrity,
                "strip_prefix": "ros2-{0}".format(commit)
            }
            with open(os.path.join(ros_version_dir, "source.json"), "w") as f:
                json.dump(ros_source_json, f, indent=4)
                f.write("\n")
                
            ros_metadata_path = os.path.join(ros_pkg_dir, "metadata.json")
            ros_metadata = {"versions": []}
            if os.path.exists(ros_metadata_path):
                with open(ros_metadata_path, 'r') as f:
                    ros_metadata = json.load(f)
            if ros_version not in ros_metadata["versions"]:
                ros_metadata["versions"].append(ros_version)
                ros_metadata["versions"].sort()
            with open(ros_metadata_path, "w") as f:
                json.dump(ros_metadata, f, indent=4)
                f.write("\n")
                
            module_content = get_copyright_header() + "\n"
            module_content += "module(\n"
            module_content += '    name = "{0}",\n'.format(ros_module_name)
            module_content += '    version = "{0}",\n'.format(ros_version)
            module_content += ")\n\n"
            module_content += "# RCR deps\n"
            module_content += 'bazel_dep(name = "rosdistro", version = "{0}.{1}")\n'.format(distro, args.ros_tag_date)
            
            pkg_names = get_package_names(distro_obj)[0]
            distribution_modules = []
            for pkg in sorted(pkg_names):
                if pkg in skip_keys or pkg in DEP_IGNORES:
                    continue

                if pkg in DEP_NAME_OVERRIDE:
                    module_content += DEP_NAME_OVERRIDE[pkg] + '\n'
                    continue

                try:
                    version = get_bazel_version(distro_obj, pkg)
                    module_content += 'bazel_dep(name = "{0}", version = "{1}")\n'.format(
                        pkg, version
                    )
                    distribution_modules.append(pkg)
                except Exception as e:
                    warn("Failed to get version for package %s: %s" % (pkg, e))

            with open(os.path.join(ros_version_dir, "MODULE.bazel"), "w") as f:
                f.write(module_content)

            distro_changes.append("Generated rosdistro and ros modules for %s" % distro)

        num_changes = 0
        for distro_name in total_changes:
            num_changes += len(total_changes[distro_name])

        if num_changes == 0:
            info('ROS distro is up to date.')
            info('Exiting...')
            clean_up()
            sys.exit(0)

        # remove duplicates
        delta = gen_delta_msg(total_changes)
        missing_deps = gen_missing_deps_msg(total_broken)

        # Commit changes and file pull request
        if args.no_commit:
            info('Skipping commit (--no-commit), changes left unstaged')
        else:
            overlay.commit_changes('all' if args.all else args.ros_distro)

        if args.dry_run:
            info('Running in dry mode, not filing PR')
            save_pr(
                overlay, delta, missing_deps=missing_deps, comment=pr_comment
            )
            sys.exit(0)
        file_pr(overlay, delta, missing_deps, comment=pr_comment)

        clean_up()
        ok('Successfully synchronized repositories!')

if __name__ == "__main__":
    main()
