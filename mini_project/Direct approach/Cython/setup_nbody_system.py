from distutils.core import setup
from Cython.Build import cythonize

setup("nbody_system_pyx", ext_modules=cythonize("nbody_system_pyx.pyx"))