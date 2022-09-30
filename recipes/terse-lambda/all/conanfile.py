from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy
from conan.tools.build import check_min_cppstd
from conan.tools.scm import Version
from conan.tools.layout import basic_layout
import os


required_conan_version = ">=1.52.0"


class TerseLambdaConan(ConanFile):
    name = "terse-lambda"
    description = "Terse lambdas for C++"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/Quincunx271/TerseLambda"
    topics = ("lambda", "macro", "header-only")
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    @property
    def _minimum_cpp_standard(self):
        return 20

    @property
    def _compilers_minimum_version(self):
        return {
            # "Visual Studio": "15", #min-version unknown
            # "msvc": "14.1", # min-version unknown
            "gcc": "10",
            "clang": "10",
            # "apple-clang": "5.1", # min-version unknown
        }

    def package_id(self):
        self.info.clear()

    def validate(self):
        if self.info.settings.get_safe("compiler.cppstd"):
            check_min_cppstd(self, self._minimum_cpp_standard)
        minimum_version = self._compilers_minimum_version.get(str(self.info.settings.compiler), False)
        if minimum_version and Version(self.info.settings.get_safe("compiler.version")) < minimum_version:
            raise ConanInvalidConfiguration(f"{self.ref} requires C++{self._minimum_cpp_standard}, which your compiler does not support.")

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
            destination=self.source_folder, strip_root=True)

    def build(self):
        pass

    def package(self):
        copy(self, pattern="LICENSE", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        copy(self, pattern="*.hpp", dst=os.path.join(self.package_folder, "include"), src=os.path.join(self.source_folder, "include"))

    def package_info(self):
        # folders not used for header-only
        self.cpp_info.bindirs = []
        self.cpp_info.frameworkdirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []

        self.cpp_info.set_property("cmake_file_name", "tl")
        self.cpp_info.set_property("cmake_target_name", "tl::tl")

        # TODO: to remove in conan v2 once cmake_find_package_* generators removed
        self.cpp_info.filenames["cmake_find_package"] = "TerseLambda"
        self.cpp_info.filenames["cmake_find_package_multi"] = "TerseLambda"
        self.cpp_info.names["cmake_find_package"] = "TerseLambda"
        self.cpp_info.names["cmake_find_package_multi"] = "TerseLambda"
