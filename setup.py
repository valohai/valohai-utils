import ast
import os
import re

import setuptools

with open(os.path.join(os.path.dirname(__file__), 'valohai', '__init__.py')) as infp:
    version = ast.literal_eval(re.search('__version__ = (.+?)$', infp.read(), re.M).group(1))

setuptools.setup(
    name="valohai-utils",
    version=version,
    author="Valohai",
    author_email="hait@valohai.com",
    license="MIT",
    packages=setuptools.find_packages(include=("valohai*",)),
    install_requires=[
        "tqdm",
        "requests",
        "valohai-yaml>=0.13.0",
    ],
)
