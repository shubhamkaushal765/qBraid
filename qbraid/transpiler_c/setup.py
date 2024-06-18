from setuptools import setup
from Cython.Build import cythonize

setup(
    name="qbraid-cython",
    ext_modules=cythonize("qbraid/transpiler_c/*.pyx", language_level=3),
    zip_safe=False,
)

# Build the cython files
# pip install cython setuptools
# python setup.py build_ext --inplace
