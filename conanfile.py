from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy
from os.path import join
import subprocess


def get_version_number() -> str:
    result = subprocess.run(
        "git describe --tags",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


class Cppgit2Conan(ConanFile):
    name = "cppgit2"
    package_type = "library"
    version = get_version_number()

    # Optional metadata
    license = "MIT"
    author = "Ricardo Benitez (benitezc.ricardo@gmail.com)"
    url = "https://github.com/ricardobtez/cppgit2.git"
    description = "A `libgit2` wrapper library for use in modern C++"
    topics = ("git", "c", "cpp", "tool")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "test/*", "samples/*", "LICENSE"
    generators = "CMakeDeps"

    def requirements(self):
        self.requires("libgit2/1.8.1")

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.19]")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake_variables = {}
        cmake.configure()
        return cmake

    def generate(self):
        toolchain = CMakeToolchain(self)
        toolchain.variables["PACKAGE_VERSION"] = self.version
        toolchain.generate()

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        if not self.conf.get("tools.build:skip_test", default=False):
            self.run(
                f"ctest --build-config {self.settings.build_type} --output-on-failure --timeout 60"
            )

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        copy(self, "LICENSE", join(self.source_folder), join(self.package_folder, "licenses"))

    def package_info(self):
        self.cpp_info.libs = ["cppgit2"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
