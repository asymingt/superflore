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
        ret = """
# Copyright {0} Open Source Robotics Foundation, Inc.
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
                 # Look up version
                 try:
                     dep_version = get_bazel_version(self.distro, dep)
                     ret += 'bazel_dep(name = "{0}", version = "{1}")\n'.format(dep, dep_version)
                     # Note: Dependency names in Bazel Registry might need a prefix like 'ros-<distro>-<pkg>'
                     # or just '<pkg>'. For now, assuming current workspace context or eventually a registry.
                     # If these are all in one giant repo, MODULE.bazel is per package.
                     # To refer to other modules, they need to be in a registry or overridden.
                 except Exception:
                     # Dep might not be in the distro (e.g. system key)
                     pass
        return ret
