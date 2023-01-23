from conans import ConanFile, CMake, tools
import os


class SlikenetConan(ConanFile):
    name = "slikenet"
    version = "0.2.0"
    license = "BSD License"
    url = "https://github.com/noizex/SLikeNet"
    description = "SLikeNet is a cross platform, open source, C++ networking engine for game programmers"
    settings = "os", "compiler", "build_type", "arch"
    options = {"fPIC": [True, False],"IPV6": [True, False],"SEC": [True, False]}
    default_options = "fPIC=True","IPV6=False","SEC=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/noizex/SLikeNet.git")
        self.run("cd SLikeNet && git checkout master")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        dir(tools)
        #tools.rmdir("SLikeNet/DependentExtensions")
        # tools.replace_in_file("RakNet/CMakeLists.txt", "project(RakNet)",
                              # '''PROJECT(RakNet)
# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# conan_basic_setup()''')
        # if self.options.IPV6:
            # tools.replace_in_file("RakNet/Source/include/slikenet/defineoverrides.h", "// USER EDITABLE FILE",
# '''// USER EDITABLE FILE
# #define RAKNET_SUPPORT_IPV6 1''')
        # if self.options.SEC:
            # tools.replace_in_file("RakNet/Source/include/slikenet/defineoverrides.h", "// USER EDITABLE FILE",
# '''// USER EDITABLE FILE
# #define LIBCAT_SECURITY 1''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions["SLIKENET_ENABLE_DEPENDENT_EXTENTIONS"] = "OFF"
        cmake.definitions["SLIKENET_ENABLE_SAMPLES"] = "OFF"
        cmake.definitions["SLIKENET_ENABLE_DLL"] = "OFF"
        cmake.definitions["SLIKENET_ENABLE_STATIC"] = "ON"
        cmake.definitions["SLIKENET_GENERATE_INCLUDE_ONLY_DIR"] = "OFF"
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.configure(source_folder="SLikeNet")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="SLikeNet/Source")
        self.copy("*.lib", dst="lib", src="Lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        #if self.options.SEC:
            #self.copy("*.*", dst="include/cat", src="RakNet/DependentExtensions/cat")
        if self.settings.compiler == "Visual Studio":
            lib_path = os.path.join(self.package_folder, "lib")
            current_lib = os.path.join(lib_path, "SLikeNetLibStaticd.lib")
            if os.path.isfile(current_lib):
                os.rename(current_lib, os.path.join(lib_path, "SLikeNetLibStatic.lib"))

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.libs = ["SLikeNetLibStatic", "pthread"]
        elif self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["SLikeNetLibStatic","ws2_32"]
        elif self.settings.os == "Macos":
            self.cpp_info.libs = ["SLikeNetLibStatic"]
