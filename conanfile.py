import os

from conans import ConanFile, tools


class SamplelibConan(ConanFile):
    name = "SampleLib"
    version = "0.0.1"
    description = "A single-header sample project"
    topics = ("header-only", "template", "sample")
    author = "Peter Lenkefi <lenkefi.peti@gmail.com>"
    license = "MIT"
    url = "https://github.com/LPeter1997/CppLibraryTemplate"
    exports = ["LICENSE"]
    exports_sources = ["single_include/*"]

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses")
        self.copy(pattern="*.hpp", dst="include", src="single_include", keep_path=True)

    def package_id(self):
        self.info.header_only()
