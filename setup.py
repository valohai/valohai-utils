import ast
import os
import re

import setuptools


def get_version():
    with open(
        os.path.join(os.path.dirname(__file__), "valohai", "__init__.py")
    ) as infp:
        match = re.search("__version__ = (.+?)$", infp.read(), re.M)
        if not match:
            raise ValueError("No version could be found")
        return ast.literal_eval(match.group(1))


setuptools.setup(
    name="valohai-utils",
    version=get_version(),
    author="Valohai",
    author_email="hait@valohai.com",
    license="MIT",
    packages=setuptools.find_packages(include=("valohai*",)),
    install_requires=["tqdm", "requests", "valohai-yaml>=0.13.0", "valohai-papi"],
    python_requires=">=3.6",
)
