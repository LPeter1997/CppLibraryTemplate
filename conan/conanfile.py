import os

from conans import ConanFile, tools


class SamplelibConan(ConanFile):
    name = "SampleProject"
    version = "0.0.1-dev"
    description = "A sample header-only C++ library template"
    topics = ("sample", "header-only", "template")
    author = "Peter Lenkefi <lenkefi.peti@gmail.com>"
    license = "MIT"
    url = "https://github.com/LPeter1997/CppLibraryTemplate"
    #exports = ["LICENSE"]
    exports_sources = ["../*"]

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses")
        self.copy(pattern="*.hpp", dst="include", src="single_include", keep_path=True)

    def package_id(self):
        self.info.header_only()
