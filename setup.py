import sys
from importlib.machinery import EXTENSION_SUFFIXES
from distutils.core import setup, Extension

from kalaha.config import __version__, __app_name__

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

extra_compile_args = []
extra_link_args = []


macros = []
if 0:
    # enable this to debug a release build
    macros.append(("VERBOSE", "1"))

CMinimax = Extension('CMinimax',
                     ['kalaha/sources/CMinimax.cpp',
                      'kalaha/sources/CNode.cpp'],
                     define_macros=macros,
                     extra_compile_args=extra_compile_args,
                     extra_link_args=extra_link_args, )

setup(name=__app_name__,
      version=__version__,
      description="Kalaha game",
      url="https://github.com/desty2k/Kalaha",
      license="MIT",
      author="Wojciech Wentland",
      author_email="wojciech.wentland@int.pl",
      long_description=long_desc,
      keywords=["cpp", "pyqt5", "minimax", "alpha-beta-pruning", "qtpy",
                "iterative-deepening-search", "kalaha", "qtpynetwork", "qrainbowstyle"],
      ext_modules=[CMinimax])
