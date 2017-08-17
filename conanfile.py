from conans.model import Generator
from conans.paths import BUILD_INFO
from conans import ConanFile

class PonyDeps(object):
    def __init__(self, conanfile):
        self.include_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                       for p in conanfile.deps_cpp_info.include_paths)
        self.lib_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                   for p in conanfile.deps_cpp_info.lib_paths)
        self.bin_paths = ",\n".join('"%s"' % p.replace("\\", "/")
                                   for p in conanfile.deps_cpp_info.bin_paths)
        self.libs = ", ".join('"%s"' % p for p in conanfile.deps_cpp_info.libs)
        self.defines = ", ".join('"%s"' % p for p in conanfile.deps_cpp_info.defines)
        self.cppflags = ", ".join('"%s"' % p for p in conanfile.deps_cpp_info.cppflags)
        self.cflags = ", ".join('"%s"' % p for p in conanfile.deps_cpp_info.cflags)
        self.sharedlinkflags = ", ".join('"%s"' % p for p in conanfile.deps_cpp_info.sharedlinkflags)
        self.exelinkflags = ", ".join('"%s"' % p for p in conanfile.deps_cpp_info.exelinkflags)

        self.rootpath = "%s" % conanfile.deps_cpp_info.rootpath.replace("\\", "/")

class Pony(Generator):
    @property
    def filename(self):
        return "build.py"

    @property
    def content(self):
        deps = PonyDeps(self.conanfile)

        template = 'paths.append({deps.include_paths})'

        sections = ["#!settings"]
        sections.append('ponyc = ["ponyc"]')
        sections.append('paths = []')

        for dep_name, dep_cpp_info in self.deps_build_info.dependencies:
            deps = PonyDeps(dep_cpp_info)
            dep_flags = template.format(dep="_" + dep_name, deps=deps)
            sections.append(dep_flags)

        sections.append("ponyc.append('--path=' + ';'.join(paths) + '')")

        sections.append("from subprocess import call")
        sections.append("call(ponyc)")

        return "\n".join(sections)


class MyCustomGeneratorPackage(ConanFile):
    name = "PonyGen"
    version = "0.1"
    url = "https://github.com/hardliner66/conan-pony"
    license = "MIT"

    def build(self):
        pass

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []