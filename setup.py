# -*- coding: utf-8 -*-
from setuptools import find_packages, setup  # noqa: H301

with open("README.md") as f:
    long_description = f.read()

NAME = "classeviva-client"
VERSION = "0.0.7"
REQUIRES = ["pydantic >= 1.9.0", "requests >= 2.25.1", "click >= 7.1.2"]

setup(
    name=NAME,
    version=VERSION,
    description="Python library and a CLI tool to access the https://web.spaggiari.eu",  # noqa: E501
    author="Maurizio Branca",
    author_email="maurizio.branca@gmail.com",
    url="https://github.com/zmoog/classeviva-client",
    scripts=["cli/classeviva"],
    keywords=[],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    classifiers=[  # https://pypi.org/classifiers/
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
