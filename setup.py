import sys
import setuptools

if sys.version_info[0] < 3 or not 5 <= sys.version_info[1] < 9:
    raise Exception("Python version must be >=3.5, <3.9")

setuptools.setup()