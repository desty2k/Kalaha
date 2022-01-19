import sys
from importlib.machinery import EXTENSION_SUFFIXES
from distutils.core import setup, Extension

from kalaha.config import __version__, __app_name__

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

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

# extra_compile_args.append("-IC:\\Program Files\\Microsoft SDKs\\Windows\\v7.0\\Include")
# extra_compile_args.append("-IC:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\include")
# extra_compile_args.append("-IC:\\Program Files (x86)\\Windows Kits\\10\\Include\\10.0.10586.0\\ucrt")
extra_compile_args.append("/DSTANDALONE")

if 0:
    # enable this to debug a release build
    extra_compile_args.append("/Od")
    extra_compile_args.append("/Z7")
    extra_link_args.append("/DEBUG")
    macros.append(("VERBOSE", "1"))

CMinimax = Extension('CMinimax',
                     ['kalaha/sources/CMinimax.cpp',
                      'kalaha/sources/CNode.cpp'],
                     define_macros=macros + [("STANDALONE", "1")],
                     extra_compile_args=extra_compile_args,
                     extra_link_args=extra_link_args, )

setup(name=__app_name__,
      version=__version__,
      description="Kalaha game",
      url="https://github.com/desty2k/Kalaha",
      license="MIT",
      author="Wojciech Wentland",
      author_email="wojciech.wentland@int.pl",
      long_description_content_type="text/markdown",
      python_requires=">=3.6",
      zip_safe=False,
      long_description=long_desc,
      keywords=["cpp", "pyqt5", "minimax", "alpha-beta-pruning", "qtpy",
                "iterative-deepening-search", "kalaha", "qtpynetwork", "qrainbowstyle"],
      ext_modules=[CMinimax])
