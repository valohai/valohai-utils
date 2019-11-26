from setuptools import find_packages, setup

from valohai import __version__

setup(
    name="valohai-utils",
    version=__version__,
    author="Valohai",
    author_email="hait@valohai.com",
    license="MIT",
    packages=find_packages(include=("valohai*",)),
)
