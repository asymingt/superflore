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

from datetime import date
from superflore.utils import get_pkg_version

# Some of the vendored ROS packages are already in the Bazel Central Registry. So,
# we override the version here to use the one from the registry.
DEP_NAME_OVERRIDE = {
    'console_bridge_vendor': 'bazel_dep(name = "console_bridge", version = "1.0.1")',
    'google_benchmark_vendor': 'bazel_dep(name = "google_benchmark", version = "1.9.4")',
    'fastcdr': 'bazel_dep(name = "fastcdr", version = "2.3.0")',
    'fastdds': 'bazel_dep(name = "fastdds", version = "3.2.2")',
    'gtest_vendor': 'bazel_dep(name = "googletest", version = "1.17.0.bcr.2")',
    'libcurl_vendor': 'bazel_dep(name = "curl", version = "8.11.0.bcr.4")',
    'libyaml_vendor': 'bazel_dep(name = "libyaml", version = "0.2.5")',
    'lz4_vendor': 'bazel_dep(name = "lz4", version = "1.10.0.bcr.1")',
    'mcap_vendor': 'bazel_dep(name = "mcap", version = "2.0.2")',
    'mimick_vendor': 'bazel_dep(name = "mimick", version = "0.9.0")',
    'pybind11_vendor': 'bazel_dep(name = "pybind11_bazel", version = "3.0.0")',
    'spdlog_vendor': 'bazel_dep(name = "spdlog", version = "1.17.0")',
    'sqlite3_vendor': 'bazel_dep(name = "sqlite3", version = "3.51.2")',
    'tinyxml2_vendor': 'bazel_dep(name = "tinyxml2", version = "10.0.0")',
    'yaml_cpp_vendor': 'bazel_dep(name = "yaml-cpp", version = "0.9.0")',
    'zenoh_cpp_vendor': 'bazel_dep(name = "zenoh-cpp", version = "1.7.2")',
    'zstd_vendor': 'bazel_dep(name = "zstd", version = "1.5.7.bcr.1")',
}

def get_bazel_version(distro, pkg_name):
    pkg = distro.release_packages[pkg_name]
    repo = distro.repositories[pkg.repository_name].release_repository
    maj_min_patch, deb_inc = repo.version.split('-')
    return "{0}.{1}-{2}".format(distro.name, maj_min_patch, deb_inc)


class BazelModule(object):
    def __init__(self, name, version, distro):
        self.name = name
        self.version = version
        self.distro = distro
        self.deps = set()

    def add_depend(self, depend, internal=True):
        if internal:
            self.deps.add(depend)
        # External deps not supported in MODULE.bazel yet unless mapped to a module

    def get_module_text(self):
        ret = """# Copyright {0} Open Source Robotics Foundation, Inc.
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

""".format(date.today().year)

        ret += "# Information about this ROS package\n"
        ret += 'module(\n'
        ret += '    name = "{0}",\n'.format(self.name)
        ret += '    version = "{0}",\n'.format(self.version)
        ret += '    bazel_compatibility = [">=7.2.1"],\n'
        ret += ')\n\n'
        ret += '# Standard Bazel rules\n'
        ret += 'bazel_dep(name = "bazel_skylib", version = "1.9.0")\n'
        ret += 'bazel_dep(name = "cmake_configure_file", version = "0.1.3")\n'
        ret += 'bazel_dep(name = "google_benchmark", version = "1.9.4")\n'
        ret += 'bazel_dep(name = "googletest", version = "1.17.0.bcr.2")\n'
        ret += 'bazel_dep(name = "platforms", version = "1.0.0")\n'
        ret += 'bazel_dep(name = "protobuf", version = "33.4")\n'
        ret += 'bazel_dep(name = "rules_cc", version = "0.2.16")\n'
        ret += 'bazel_dep(name = "rules_python", version = "1.8.3")\n'
        ret += 'bazel_dep(name = "rules_rust", version = "0.68.1")\n'
        ret += 'bazel_dep(name = "rules_shell", version = "0.6.1")\n'

        if self.deps:
             ret += '\n# ROS Dependencies\n'
             for dep in sorted(self.deps):
                 try:
                    if dep in DEP_NAME_OVERRIDE:
                        ret += DEP_NAME_OVERRIDE[dep] + '\n'
                    else:
                        dep_version = get_bazel_version(self.distro, dep)
                        ret += 'bazel_dep(name = "{0}", version = "{1}")\n'.format(dep, dep_version)
                 except Exception:
                    pass
        return ret


    def get_source_json(self, url, integrity, strip_prefix):
        return {
            "integrity": integrity,
            "url": url,
            "strip_prefix": strip_prefix,
        }

    def get_metadata_json(self, homepage, maintainers, versions, yanked_versions=None):
        return {
            "homepage": homepage,
            "maintainers": maintainers,
            "versions": versions,
            "yanked_versions": yanked_versions or {},
        }
