import os
os.environ["MLK_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"


from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np


ext_modules=[
    Extension("openmp_nbody_system_pyx", ["openmp_nbody_system_pyx.pyx"],
            include_dirs=[np.get_include()],
            extra_compile_args=['-fopenmp'],
            extra_link_args=['-fopenmp']),
]

setup(name="openmp_nbody_system_pyx",
      ext_modules=cythonize(ext_modules))
