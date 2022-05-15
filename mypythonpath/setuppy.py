
from distutils.core import setup
from Cython.Build import cythonize

# setup(ext_modules=cythonize(["killdll.py"]))
setup(ext_modules=cythonize(["jxtest.py"]))
