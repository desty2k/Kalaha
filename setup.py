import sys
from importlib.machinery import EXTENSION_SUFFIXES
from distutils.core import setup, Extension

if sys.version_info < (3, 9):
    python_dll_name = '\\"python%d%d.dll\\"' % sys.version_info[:2]
    python_dll_name_debug = '\\"python%d%d_d.dll\\"' % sys.version_info[:2]
else:
    python_dll_name = '\"python%d%d.dll\"' % sys.version_info[:2]
    python_dll_name_debug = '\"python%d%d_d.dll\"' % sys.version_info[:2]

if "_d.pyd" in EXTENSION_SUFFIXES:
    macros = [("PYTHONDLL", python_dll_name_debug),
              # ("PYTHONCOM", '\\"pythoncom%d%d_d.dll\\"' % sys.version_info[:2]),
              ("_CRT_SECURE_NO_WARNINGS", '1')]
else:
    macros = [("PYTHONDLL", python_dll_name),
              # ("PYTHONCOM", '\\"pythoncom%d%d.dll\\"' % sys.version_info[:2]),
              ("_CRT_SECURE_NO_WARNINGS", '1'), ]

extra_compile_args = []
extra_link_args = []

extra_compile_args.append("-IC:\\Program Files\\Microsoft SDKs\\Windows\\v7.0\\Include")
extra_compile_args.append("-IC:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\include")
extra_compile_args.append("-IC:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.10586.0\\ucrt")
extra_compile_args.append("/DSTANDALONE")

if 0:
    # enable this to debug a release build
    extra_compile_args.append("/Od")
    extra_compile_args.append("/Z7")
    extra_link_args.append("/DEBUG")
    macros.append(("VERBOSE", "1"))

cautoplayer = Extension('CAutoPlayer',
                        ['kalaha/sources/CAutoPlayer.cpp',
                         'kalaha/sources/CNode.cpp'],
                        define_macros=macros + [("STANDALONE", "1")],
                        extra_compile_args=extra_compile_args,
                        extra_link_args=extra_link_args,)

setup(name='CAutoPlayer',
      version='0.1.0',
      description='Kalaha auto player written in C++',
      ext_modules=[cautoplayer])
