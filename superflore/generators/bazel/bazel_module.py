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

DEFAULT_DEPS = {
    'bazel_dep(name = "aspect_rules_py", version = "1.9.1")',
    'bazel_dep(name = "bazel_skylib", version = "1.9.0")',
    'bazel_dep(name = "cmake_configure_file", version = "0.1.6")',
    'bazel_dep(name = "platforms", version = "1.0.0")',
    'bazel_dep(name = "protobuf", version = "34.0.bcr.1")',
    'bazel_dep(name = "rules_cc", version = "0.2.17")',
    'bazel_dep(name = "rules_python", version = "1.9.0")',
    'bazel_dep(name = "rules_rs", version = "0.0.43")',
    'bazel_dep(name = "rules_rust", version = "0.69.0")',
    'bazel_dep(name = "rules_shell", version = "0.6.1")',
}

PCL_DEPS = {
    'bazel_dep(name = "pcl", version = "1.15.1.bcr.3")'
}

QT5_DEPS = {
    'bazel_dep(name = "rules_qt", version = "0.0.6")'
}

QT6_DEPS = {
    'bazel_dep(name = "rules_qt", version = "0.0.6")'
}

BOOST_DEPS = {
    'bazel_dep(name = "boost.algorithm", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.align", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.any", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.array", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.asio", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.assert", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.assign", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.atomic", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.beast", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.bimap", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.bind", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.callable_traits", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.charconv", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.chrono", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.circular_buffer", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.compat", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.compatibility", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.compute", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.concept_check", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.config", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.container", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.container_hash", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.context", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.conversion", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.core", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.coroutine", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.coroutine2", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.crc", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.date_time", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.describe", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.detail", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.dll", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.dynamic_bitset", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.endian", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.exception", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.filesystem", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.foreach", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.format", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.function", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.functional", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.function_types", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.fusion", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.geometry", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.graph", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.hash2", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.heap", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.hof", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.icl", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.integer", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.interprocess", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.intrusive", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.io", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.iostreams", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.iterator", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.json", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.lambda", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.lambda2", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.leaf", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.lexical_cast", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.locale", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.lockfree", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.log", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.logic", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.math", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.move", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.mp11", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.mpl", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.mqtt5", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.multi_array", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.multi_index", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.multiprecision", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.mysql", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.numeric_conversion", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.numeric_interval", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.numeric_ublas", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.optional", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.parameter", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.pfr", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.phoenix", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.pin_version", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.polygon", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.pool", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.predef", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.preprocessor", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.process", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.program_options", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.property_map", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.property_tree", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.proto", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.ptr_container", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.python", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.qvm", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.random", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.range", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.ratio", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.rational", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.regex", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.scope", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.scope_exit", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.serialization", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.signals2", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.smart_ptr", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.sort", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.spirit", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.stacktrace", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.static_assert", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.static_string", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.system", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.test", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.thread", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.throw_exception", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.timer", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.tokenizer", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.tti", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.tuple", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.type_index", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.typeof", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.type_traits", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.units", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.unordered", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.url", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.utility", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.uuid", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.variant", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.variant2", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.vmd", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.winapi", version = "1.90.0.bcr.1")',
    'bazel_dep(name = "boost.xpressive", version = "1.90.0.bcr.1")',
}

# Some of the vendored ROS packages are already in the Bazel Central Registry. So,
# we override the version here to use the one from the registry.
DEP_NAME_OVERRIDE = {
    'asio': 'bazel_dep(name = "asio", version = "1.34.2.bcr.0")',
    'assimp-dev' : 'bazel_dep(name = "assimp", version = "6.0.3")',
    'assimp' : 'bazel_dep(name = "assimp", version = "6.0.3")',
    'autoconf': 'bazel_dep(name = "rules_autoconf", version = "0.0.16")',
    'automake': 'bazel_dep(name = "rules_foreign_cc", version = "0.15.1")',
    'aws_sdk_vendor': 'bazel_dep(name = "aws_sdk", version = "1.11.321.bcr.0")',
    'bullet': 'bazel_dep(name = "bullet", version = "3.26.0-rc0.bcr.1")',
    'bzip2': 'bazel_dep(name = "bzip2", version = "1.0.8.bcr.4")',
    'cargo': 'bazel_dep(name = "rules_rust", version = "0.69.0")',
    'catch2': 'bazel_dep(name = "catch2", version = "3.13.0")',
    'cli11': 'bazel_dep(name = "cli11", version = "2.5.0")',
    'console_bridge_vendor': 'bazel_dep(name = "console_bridge", version = "1.0.1")',
    'curl': 'bazel_dep(name = "curl", version = "8.12.0")',
    'doxygen': 'bazel_dep(name = "rules_doxygen", version = "2.6.2")',
    'eigen': 'bazel_dep(name = "eigen", version = "5.0.1.bcr.1")',
    'fastcdr': 'bazel_dep(name = "fastcdr", version = "2.3.5.bcr.0")',
    'fastdds': 'bazel_dep(name = "fastdds", version = "3.4.2")',
    'ffmpeg' : 'bazel_dep(name = "ffmpeg", version = "7.1.1.bcr.beta.2")',
    'file': 'bazel_dep(name = "libmagic", version = "5.46.bcr.4")',
    'fmt': 'bazel_dep(name = "fmt", version = "12.1.0")',
    'geographiclib-tools': 'bazel_dep(name = "geographiclib", version = "2.4.0.bcr.2")',
    'geographiclib': 'bazel_dep(name = "geographiclib", version = "2.4.0.bcr.2")',
    'git': 'bazel_dep(name = "git", version = "2.53.0.bcr.1")',
    'gmock_vendor': 'bazel_dep(name = "googletest", version = "1.17.0.bcr.2")',
    'google_benchmark_vendor': 'bazel_dep(name = "google_benchmark", version = "1.9.4")',
    'google-mock': 'bazel_dep(name = "googletest", version = "1.17.0.bcr.2")',
    'gtest_vendor': 'bazel_dep(name = "googletest", version = "1.17.0.bcr.2")',
    'gtest': 'bazel_dep(name = "googletest", version = "1.17.0.bcr.2")',
    'gz_common_vendor': 'bazel_dep(name = "gz-common", version = "7.1.0")',
    'gz_dartsim_vendor': 'bazel_dep(name = "dartsim", version = "6.13.2.bcr.2")',
    'gz_fuel_tools_vendor': 'bazel_dep(name = "gz-fuel-tools", version = "11.0.0")',
    'gz_math_vendor': 'bazel_dep(name = "gz-math", version = "9.0.0")',
    'gz_msgs_vendor': 'bazel_dep(name = "gz-msgs", version = "12.0.1")',
    'gz_ogre_next_vendor': 'bazel_dep(name = "ogre-next", version = "2.3.3.bcr.2")',
    'gz_physics_vendor': 'bazel_dep(name = "gz-physics", version = "9.1.0")',
    'gz_plugin_vendor': 'bazel_dep(name = "gz-plugin", version = "4.0.0")',
    'gz_rendering_vendor': 'bazel_dep(name = "gz-rendering", version = "10.0.1")',
    'gz_sensors_vendor': 'bazel_dep(name = "gz-sensors", version = "10.0.1")',
    'gz_sim_vendor': 'bazel_dep(name = "gz-sim", version = "10.1.1")',
    'gz_transport_vendor': 'bazel_dep(name = "gz-transport", version = "15.0.2")',
    'gz_utils_vendor': 'bazel_dep(name = "gz-utils", version = "4.0.0")',
    'lcov': 'bazel_dep(name = "lcov", version = "2.3.2")',
    'libabsl-dev': 'bazel_dep(name = "abseil-cpp", version = "20260107.1")',
    'libcairo2-dev': 'bazel_dep(name = "cairo", version = "1.18.4")',
    'libcap-dev': 'bazel_dep(name = "libcap", version = "2.27.bcr.1")',
    'libccd-dev': 'bazel_dep(name = "ccd", version = "2.1.0.bcr.1")',
    'libceres-dev': 'bazel_dep(name = "ceres-solver", version = "2.2.0")',
    'libconsole-bridge-dev': 'bazel_dep(name = "console_bridge", version = "1.0.1")',
    'libcurl_vendor': 'bazel_dep(name = "curl", version = "8.11.0.bcr.4")',
    'libcurl-dev': 'bazel_dep(name = "curl", version = "8.12.0")',
    'libfcl-dev': 'bazel_dep(name = "fcl", version = "0.7.0.bcr.2")',
    'libfcl': 'bazel_dep(name = "fcl", version = "0.7.0.bcr.2")',
    'libflann-dev': 'bazel_dep(name = "flann", version = "1.9.2")',
    'libgflags-dev': 'bazel_dep(name = "gflags", version = "2.2.2.bcr.1")',
    'libglew-dev': 'bazel_dep(name = "glew", version = "2.3.1")',
    'libglfw3-dev': 'bazel_dep(name = "glfw", version = "3.4.0.bcr.1")',
    'libgoogle-glog-dev': 'bazel_dep(name = "glog", version = "0.7.1.bcr.1")',
    'libicu-dev': 'bazel_dep(name = "icu", version = "78.2")',
    'libjpeg': 'bazel_dep(name = "libjpeg_turbo", version = "3.1.3.bcr.4")',
    'libjsoncpp-dev': 'bazel_dep(name = "jsoncpp", version = "1.9.6.bcr.1")',
    'libjsoncpp-dev': 'bazel_dep(name = "jsoncpp", version = "1.9.6.bcr.1")',
    'libjsoncpp': 'bazel_dep(name = "jsoncpp", version = "1.9.6.bcr.1")',
    'liblttng-ctl-dev': 'bazel_dep(name = "lttng-ust", version = "2.14.0")',
    'liblttng-ust-dev': 'bazel_dep(name = "lttng-ust", version = "2.14.0")',
    'liblz4_vendor': 'bazel_dep(name = "lz4", version = "1.10.0.bcr.1")',
    'libmodbus-dev': 'bazel_dep(name = "libmodbus", version = "3.1.11.bcr.1")',
    'libncurses-dev': 'bazel_dep(name = "ncurses", version = "6.4.20221231.bcr.11")',
    'libnlopt-cxx-dev': 'bazel_dep(name = "nlopt", version = "2.7.1")',
    'liboctomap-dev': 'bazel_dep(name = "octomap", version = "1.10.0")',
    'libogg': 'bazel_dep(name = "ogg", version = "1.3.5")',
    'libopencv-dev': 'bazel_dep(name = "opencv", version = "4.13.0.bcr.5")',
    'libopencv-imgproc-dev': 'bazel_dep(name = "opencv", version = "4.13.0.bcr.5")',
    'libpaho-mqtt-dev': 'bazel_dep(name = "paho.mqtt.cpp", version = "1.5.2")',
    'libpaho-mqttpp-dev': 'bazel_dep(name = "paho.mqtt.cpp", version = "1.5.2")',
    'libpcap-dev': 'bazel_dep(name = "libpcap", version = "1.10.5")',
    'libpcap': 'bazel_dep(name = "libpcap", version = "1.10.5")',
    'libpcl-all-dev': 'bazel_dep(name = "pcl", version = "1.15.1.bcr.3")',
    'libpng-dev': 'bazel_dep(name = "libpng", version = "1.6.54")',
    'libpoco-dev': 'bazel_dep(name = "poco", version = "1.14.2-20250528.bcr.1")',
    'libqhull': 'bazel_dep(name = "qhull", version = "8.0.2")',
    'libsqlite3-dev': 'bazel_dep(name = "sqlite3", version = "3.51.2")',
    'libssl-dev': 'bazel_dep(name = "openssl", version = "3.5.5.bcr.1")',
    'libturbojpeg': 'bazel_dep(name = "libjpeg_turbo", version = "3.1.3.bcr.4")',
    'liburdfdom-headers-dev': 'bazel_dep(name = "urdfdom_headers", version = "1.0.5")',
    'liburdfdom-tools': 'bazel_dep(name = "urdfdom", version = "2.3.4.bcr.1")',
    'libusb-1.0-dev': 'bazel_dep(name = "libusb", version = "1.0.28")',
    'libusb-1.0': 'bazel_dep(name = "libusb", version = "1.0.28")',
    'libusb-dev': 'bazel_dep(name = "libusb", version = "1.0.28")',
    'libwebsocketpp-dev': 'bazel_dep(name = "websocketpp", version = "0.8.2.bcr.6")',
    'libx11-dev': 'bazel_dep(name = "libx11", version = "1.8.12.bcr.5")',
    'libx11': 'bazel_dep(name = "libx11", version = "1.8.12.bcr.5")',
    'libxi-dev': 'bazel_dep(name = "libxi", version = "1.8.2")',
    'libxkbcommon-dev': 'bazel_dep(name = "xkbcommon", version = "1.9.2.bcr.beta.1")',
    'libxml2-utils': 'bazel_dep(name = "libxml2", version = "2.15.1.bcr.1")',
    'libxml2': 'bazel_dep(name = "libxml2", version = "2.15.1.bcr.1")',
    'libxrandr': 'bazel_dep(name = "libxrandr", version = "1.5.4")',
    'libyaml_vendor': 'bazel_dep(name = "libyaml", version = "0.2.5")',
    'libzmq3-dev': 'bazel_dep(name = "libzmq", version = "4.3.5.bcr.4")',
    'libzstd-dev': 'bazel_dep(name = "zstd", version = "1.5.7.bcr.1")',
    'lttng-tools': 'bazel_dep(name = "lttng-ust", version = "2.14.0")',
    'lua-dev': 'bazel_dep(name = "lua", version = "5.5.0")',
    'lua5.2-dev': 'bazel_dep(name = "lua", version = "5.5.0")',
    'lz4': 'bazel_dep(name = "lz4", version = "1.10.0.bcr.1")',
    'lz4_vendor': 'bazel_dep(name = "lz4", version = "1.10.0.bcr.1")',
    'magic_enum': 'bazel_dep(name = "magic_enum", version = "0.9.7")',
    'mcap_vendor': 'bazel_dep(name = "mcap", version = "2.0.2")',
    'meson': 'bazel_dep(name = "meson", version = "1.5.1")',
    'mimick_vendor': 'bazel_dep(name = "mimick", version = "0.9.0")',
    'mp_units_vendor': 'bazel_dep(name = "mp-units", version = "2.5.0.bcr.0")',
    'nanobind-dev': 'bazel_dep(name = "nanobind", version = "2.9.2")',
    'nlohmann-json-dev': 'bazel_dep(name = "nlohmann_json", version = "3.12.0.bcr.1")',
    'openssl': 'bazel_dep(name = "openssl", version = "3.5.5.bcr.1")',
    'protobuf-dev': 'bazel_dep(name = "protobuf", version = "34.0.bcr.1")',
    'protobuf': 'bazel_dep(name = "protobuf", version = "34.0.bcr.1")',
    'pugixml-dev': 'bazel_dep(name = "pugixml", version = "1.15")',
    'pugixml': 'bazel_dep(name = "pugixml", version = "1.15")',
    'pybind11_vendor': 'bazel_dep(name = "pybind11_bazel", version = "3.0.0")',
    'pybind11-dev': 'bazel_dep(name = "pybind11_bazel", version = "3.0.0")',
    'range-v3': 'bazel_dep(name = "range-v3", version = "0.12.0")',
    'rapidjson-dev': 'bazel_dep(name = "rapidjson", version = "1.1.0.bcr.20250205")',
    'sdformat_vendor': 'bazel_dep(name = "sdformat", version = "16.0.1")',
    'simde': 'bazel_dep(name = "simde", version = "0.8.2")',
    'spdlog_vendor': 'bazel_dep(name = "spdlog", version = "1.17.0")',
    'spdlog': 'bazel_dep(name = "spdlog", version = "1.17.0")',
    'sqlite3_vendor': 'bazel_dep(name = "sqlite3", version = "3.51.2")',
    'sqlite3': 'bazel_dep(name = "sqlite3", version = "3.51.2")',
    'suitesparse': 'bazel_dep(name = "suitesparse", version = "7.10.1.bcr.3")',
    'swig': 'bazel_dep(name = "swig", version = "4.3.0.bcr.2")',
    'tbb': 'bazel_dep(name = "onetbb", version = "2022.2.0")',
    'tinyxml_vendor': 'bazel_dep(name = "tinyxml", version = "2.6.2.bcr.1")',
    'tinyxml2_vendor': 'bazel_dep(name = "tinyxml2", version = "10.0.0")',
    'tinyxml2': 'bazel_dep(name = "tinyxml2", version = "10.0.0")',
    'unzip' : 'bazel_dep(name = "zip", version = "3.0")',
    'uuid': 'bazel_dep(name = "libuuid", version = "2.41.2")',
    'wayland-dev': 'bazel_dep(name = "wayland", version = "1.24.0.bcr.1")',
    'wayland': 'bazel_dep(name = "wayland", version = "1.24.0.bcr.1")',
    'xacro': 'bazel_dep(name = "xacro", version = "2.0.12")',
    'yaml_cpp_vendor': 'bazel_dep(name = "yaml-cpp", version = "0.9.0")',
    'yaml-cpp': 'bazel_dep(name = "yaml-cpp", version = "0.9.0")',
    'yaml': 'bazel_dep(name = "libyaml", version = "0.2.5")',
    'zenoh_cpp_vendor': 'bazel_dep(name = "zenoh-cpp", version = "1.7.2")',
    'zlib': 'bazel_dep(name = "zlib", version = "1.3.2")',
    'zstd_vendor': 'bazel_dep(name = "zstd", version = "1.5.7.bcr.1")',
}

DEP_IGNORES = [
    "acado_vendor",
    "acl",
    "action_tutorials_interfaces",
    "actionlib_msgs",
    "ads_vendor",
    "ament_cmake_vendor_package",
    "aws_sdk_cpp_vendor",
    "benchmark",
    "binutils",
    "black",
    "boost_sml_vendor",
    "clang-format",
    "clang-tidy",
    "clang",
    "clips_vendor",
    "cmake",
    "coinor-libipopt-dev",
    "cppcheck",
    "cwiid-dev",
    "cwiid",
    "dkms",
    "dpkg",
    "fmilibrary_vendor",
    "foonathan_memory_vendor",
    "gazebo_ros_pkgs",
    "gdal",
    "geos",
    "glut",
    "graphviz",
    "gurumdds-3.2",
    "gz_cmake_vendor",
    "gz_cmake_vendor",
    "gz_gui_vendor",
    "gz_gui_vendor",
    "gz_launch_vendor",
    "gz_launch_vendor",
    "gz_tools_vendor",
    "gz_tools_vendor",
    "hash_library_vendor",
    "iwyu",
    "jupyter-notebook",
    "libatomic",
    "libavahi-client-dev",
    "libavdevice-dev",
    "libbluetooth-dev",
    "libbluetooth",
    "libcaer_vendor",
    "libclang-dev",
    "libdbus-dev",
    "libdraco-dev",
    "libdw-dev",
    "libepoxy-dev",
    "libfreenect-dev",
    "libgdal-dev",
    "libgeos++-dev",
    "libgps",
    "libgstreamer-plugins-base1.0-dev",
    "libgstreamer1.0-dev",
    "libjson-c-dev",
    "liblapack-dev",
    "liblapack-dev",
    "libomp-dev",
    "libopenni2-dev",
    "liborocos-kdl-dev",
    "liborocos-kdl",
    "libqwt-qt5-dev",
    "libserial-dev",
    "libspnav-dev",
    "libtheora",
    "libtins-dev",
    "libtool",
    "libudev-dev",
    "libv4l-dev",
    "libxmlrpc-c++",
    "libxmu-dev",
    "libxxf86vm",
    "libyuv-dev",
    "live555_vendor",
    "lm-sensors",
    "matio",
    "menge_vendor",
    "mujoco_vendor",
    "muparser",
    "nlohmann_json_schema_validator_vendor",
    "ocl-icd-opencl-dev",
    "omp",
    "open3d_vendor",
    "opencl-headers",
    "openeb_vendor",
    "opengl",
    "orocos_kdl_vendor",
    "ortools_vendor",
    "osqp_vendor",
    "pkg-config",
    "proj",
    "pybind11_json_vendor",
    "pybind11-json-dev",
    "pydocstyle",
    "pyflakes3",
    "python_orocos_kdl_vendor",
    "python-argparse",
    "python3",
    "qml-module-qtquick2",
    "qml6-module-qtqml-workerscript",
    "qml6-module-qtquick",
    "qpoases_vendor",
    "ros_ign_bridge",
    "ros_ign_gazebo",
    "rti-connext-dds-7.3.0",
    "rviz_ogre_vendor",
    "sdl2_vendor",
    "socat",
    "sol_vendor",
    "spacenavd",
    "tango_icons_vendor",
    "tinyspline_vendor",
    "tvm_vendor",
    "udev",
    "uncrustify_vendor",
    "v4l-utils",
    "wget",
    "wx-common",
    "wxwidgets",
    "xclip",
    "zbar",
    "zmqpp_vendor",
]

def get_bazel_version(distro, pkg_name):
    pkg = distro.release_packages[pkg_name]
    repo = distro.repositories[pkg.repository_name].release_repository
    maj_min_patch, deb_inc = repo.version.split('-')
    return "{0}.{1}-{2}".format(distro.name, maj_min_patch, deb_inc)

def get_copyright_header():
    return """# Copyright {0} Open Source Robotics Foundation, Inc.
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

class BazelModule(object):
    def __init__(self, name, version, distro):
        self.name = name
        self.version = version
        self.distro = distro
        self.deps = set()
        self.bcr_deps = DEFAULT_DEPS

    def add_depend(self, depend, internal=True):
        is_boost = depend.startswith("libboost-") \
            or depend.startswith("boost")
        is_qt5 = depend.startswith("libqt5") \
            or depend.startswith("qt5") \
            or depend.startswith("qtbase5") \
            or depend.startswith("qttools5") \
            or depend.startswith("qtdeclarative5") \
            or depend.startswith("qtmultimedia5") \
            or depend.startswith("pyqt5")
        is_qt6 = depend.startswith("libqt6") \
            or depend.startswith("qt6") \
            or depend.startswith("qtbase6") \
            or depend.startswith("qttools6") \
            or depend.startswith("qtdeclarative6") \
            or depend.startswith("qtmultimedia6") \
            or depend.startswith("pyqt6")
        is_pcl = depend.startswith("pcl") \
            or depend.startswith("libpcl")
        is_python = depend.startswith("python3-") \
            or depend.startswith("python-")
        is_ignored = depend in DEP_IGNORES
        is_bcr = depend in DEP_NAME_OVERRIDE.keys()
        if internal:
            self.deps.add(depend)
        elif is_bcr:
            self.bcr_deps.add(DEP_NAME_OVERRIDE[depend])
        elif is_boost:
            self.bcr_deps.update(BOOST_DEPS)
        elif is_qt5:
            self.bcr_deps.update(QT5_DEPS)
        elif is_qt6:
            self.bcr_deps.update(QT6_DEPS)
        elif is_pcl:
            self.bcr_deps.update(PCL_DEPS)
        elif is_python or is_ignored:
            pass
        else:
            raise RuntimeError(f"Unknown key: {depend}")

    def get_module_text(self):
        ret = get_copyright_header()
        ret += "# ROS package information\n"
        ret += 'module(\n'
        ret += '    name = "{0}",\n'.format(self.name)
        ret += '    version = "{0}",\n'.format(self.version)
        ret += '    bazel_compatibility = [">=7.2.1"],\n'
        ret += ')\n\n'
        ret += '# BCR dependencies\n'
        for dep in sorted(self.bcr_deps):
            ret += dep + '\n'
        if self.deps:
             ret += '\n# RCR Dependencies\n'
             for dep in sorted(self.deps):
                 try:
                    if dep in DEP_NAME_OVERRIDE:
                        ret += DEP_NAME_OVERRIDE[dep] + '\n'
                    elif dep not in DEP_IGNORES:
                        dep_version = get_bazel_version(self.distro, dep)
                        ret += 'bazel_dep(name = "{0}", version = "{1}")\n'.format(dep, dep_version)
                 except Exception:
                    pass
        return ret


    def get_source_json(self, url, integrity, strip_prefix, overlay=None, patches=None, patch_cmds=None):
        result = {
            "integrity": integrity,
            "url": url,
            "strip_prefix": strip_prefix,
        }
        if overlay:
            result["overlay"] = overlay
        if patches:
            result["patches"] = patches
            result["patch_strip"] = 1
        if patch_cmds:
            result["patch_cmds"] = patch_cmds
        return result
