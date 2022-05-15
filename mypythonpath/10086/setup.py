
#!python
#cython: language_level=3
# import cython

# @cython.language_level("3")
# def do_something():
#     pass
# from distutils.core import setup
# from distutils.extension import Extension
# from Cython.Build import cythonize
# import sys
# passing 3 or 2 as integer is also accepted:
# cythonize(Extension, compiler_directives={'language_level' : sys.version_info[0]})

# setup(ext_modules=cythonize(["webdriver_test.py"]))

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("ccgpcq",  ["ccgp_cq.py"]),
]

setup(
    name = 'wwdd',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
