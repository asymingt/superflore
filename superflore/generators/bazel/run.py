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
                    current, current_info, pkg = regenerate_pkg(
                        overlay,
                        pkg,
                        get_distro(args.ros_distro),
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

            # Generate release files
            release_dir = os.path.join(
                overlay.repo.repo_dir, "releases", distro, args.ros_tag_date
            )
            make_dir(release_dir)

            module_content =  get_copyright_header() + "\n"
            module_content += """# Every ROS workspace must declare itself as a module.
module(
    name = "{name}",
    version = "{version}",
)

# BCR deps
{bcr_deps}
bazel_dep(name = "toolchains_llvm", version = "1.6.0")

# RCR deps
""".format(name=args.ros_distro, version=args.ros_tag_date, bcr_deps="\n".join(DEFAULT_DEPS))
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

            module_content += """
# A lot of the tooling for IDL generation requires a Python 3.12 toolchain
# to work. You need to configure your workspace correctly to provide one.

python = use_extension("@rules_python//python/extensions:python.bzl", "python")
python.toolchain(
    python_version = "3.11",
    is_default = True,
)

# Having a self-contained C++ toolchain prevents bazel from polling PATH
# for a compiler, making the builds less reliant on the host environment.

llvm = use_extension("@toolchains_llvm//toolchain/extensions:llvm.bzl", "llvm")
llvm.toolchain(llvm_version = "20.1.7")
use_repo(llvm, "llvm_toolchain")

register_toolchains("@llvm_toolchain//:all")

# Uncomment when writing release patches.
# include("//:dev.MODULE.bazel")

"""

            with open(os.path.join(release_dir, "MODULE.bazel"), "w") as f:
                f.write(module_content)

            with open(os.path.join(release_dir, "BUILD.bazel"), "w") as f:
                f.write(get_copyright_header())

            with open(os.path.join(release_dir, ".bazelversion"), "w") as f:
                f.write("9.0.0")

            with open(os.path.join(release_dir, ".bazelignore"), "w") as f:
                f.write("vanilla\n")

            with open(os.path.join(release_dir, ".bazelrc"), "w") as f:
                f.write(get_copyright_header())
                f.write("""
# Augment the BCR with a few of our own modules in the docs folder.
common --registry=file://%workspace%/../../..        --registry=https://bcr.bazel.build

# Remote cache.
common --remote_cache=https://storage.googleapis.com/intrinsic-opensource-buildcache
common --remote_upload_local_results=false
common --remote_cache_compression=true

# Define ROS_HOME so that tests don't try and write to ~/.ros_home by default.
common --test_env=ROS_HOME=".ros"

# Force Bazel to stop producing implicit __init__.py files in Python. This
# is so that we can use PEP420 namespace package feature for IDL generation.
common --incompatible_default_to_explicit_init_py

# Force Bazel to use an environment with a static value for PATH, and not to
# use the LD_LIBRARY_PATH. This makes builds robust to terminal refreshes.
common --incompatible_strict_action_env

# The zenoh tests must be allowed to contact the network to communicate with
# the zenohd router, or else they will fail.
test --sandbox_default_allow_network=true

# Use C++17 standard by default across the whole repo.
build --cxxopt="-std=c++17"

# Ensure that we use toolchains_llvm instead of the host toolchain.
build --action_env="BAZEL_DO_NOT_DETECT_CPP_TOOLCHAIN=1"

# Tell Bazel to use the pre-compiled binary instead of building from source
build --@protobuf//bazel/toolchains:prefer_prebuilt_protoc

# ASAN
build:asan --strip=never
build:asan --copt=-fsanitize=address
build:asan --copt=-O0
build:asan --copt=-fno-omit-frame-pointer
build:asan --linkopt=-fsanitize=address

# MSAN
build:msan --strip=never
build:msan --copt=-fsanitize=memory
build:msan --copt=-O0
build:msan --copt=-fno-omit-frame-pointer
build:msan --linkopt=-fsanitize=memory

# TSAN
build:tsan --strip=never
build:tsan --copt=-fsanitize=thread
build:tsan --copt=-O0
build:tsan --copt=-fno-omit-frame-pointer
build:tsan --linkopt=-fsanitize=thread

# Allow for local testing of distribution.
common:distribution --target_pattern_file=distribution.txt

# Vendoring for development
""")
                # Write vendor stanza with --repo for each module
                if distribution_modules:
                    vendor_lines = ['vendor --vendor_dir=vendor']
                    for mod in distribution_modules:
                        vendor_lines.append('    --repo=@{0}'.format(mod))
                    # Join with ' \\\n' for line continuation, except the last line
                    f.write(' \\\n'.join(vendor_lines))
                    f.write('\n')

            with open(os.path.join(release_dir, "distribution.txt"), "w") as f:
                for mod in distribution_modules:
                    f.write("@{0}//...\n".format(mod))

            with open(os.path.join(release_dir, "dev.MODULE.bazel"), "w") as f:
                f.write(get_copyright_header())
                for mod in distribution_modules:
                    f.write('local_path_override(\n')
                    f.write('    module_name = "{0}",\n'.format(mod))
                    f.write('    path = "./vendor/{0}+",\n'.format(mod))
                    f.write(')\n')

            # Generate vendor/VENDOR.bazel with ignore() for all BCR deps
            vendor_dir = os.path.join(release_dir, "vendor")
            make_dir(vendor_dir)
            bcr_names = set(['toolchains_llvm'])
            for dep in DEFAULT_DEPS:
                m = re.search(r'name\s*=\s*"([^"]+)"', dep)
                if m:
                    bcr_names.add(m.group(1))
            for dep_str in DEP_NAME_OVERRIDE.values():
                m = re.search(r'name\s*=\s*"([^"]+)"', dep_str)
                if m:
                    bcr_names.add(m.group(1))
            with open(os.path.join(vendor_dir, "VENDOR.bazel"), "w") as f:
                f.write('###############################################################################\n')
                f.write('# This file is used to configure how external repositories are handled in vendor mode.\n')
                f.write('# ONLY the two following functions can be used:\n')
                f.write('#\n')
                f.write("# ignore('@@<canonical repo name>', ...) is used to completely ignore this repo from vendoring.\n")
                f.write('# Bazel will use the normal external cache and fetch process for this repo.\n')
                f.write('#\n')
                f.write("# pin('@@<canonical repo name>', ...) is used to pin the contents of this repo under the vendor\n")
                f.write('# directory as if there is a --override_repository flag for this repo.\n')
                f.write('# Note that Bazel will NOT update the vendored source for this repo while running vendor command\n')
                f.write("# unless it's unpinned. The user can modify and maintain the vendored source for this repo manually.\n")
                f.write('###############################################################################\n')
                f.write('\n')
                for name in sorted(bcr_names):
                    f.write('ignore("@@{0}")\n'.format(name))

            distro_changes.append("Generated release artifacts for %s" % release_dir)

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
