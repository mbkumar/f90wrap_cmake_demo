import sys

from skbuild import setup

setup(
    name="cylinder",
    version="0.0.1",
    packages=["cylinder"],

    install_requires=['f90wrap']
)
