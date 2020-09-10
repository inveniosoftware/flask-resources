# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Flask-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Flask Resources module to create REST APIs."""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = [
    "black>=20.8b1,<20.9b0",
    "check-manifest>=0.25",
    # coverage pinned because of https://github.com/nedbat/coveragepy/issues/716
    "coverage>=4.0,<5.0.0",
    "isort>=5.0,<6.0",
    "pydocstyle~=5.0.0",
    "pytest>=4.6.1",
    "pytest-cov>=2.5.1",
    "pytest-flask>=0.15.1,<1.0.0",
    "pytest-mock>=1.6.0",
    "pytest-pep8>=1.0.6",
]

extras_require = {
    "docs": ["Sphinx>=1.5.1,<3",],
    "tests": tests_require,
}

extras_require["all"] = []
for reqs in extras_require.values():
    extras_require["all"].extend(reqs)

setup_requires = ["Babel>=1.3"]

install_requires = [
    "Flask~=1.1.2",
    "webargs~=5.5.0",
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("flask_resources", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="flask-resources",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords="flask TODO",
    license="MIT",
    author="CERN",
    author_email="info@inveniosoftware.org",
    url="https://github.com/inveniosoftware/flask-resources",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={},
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 1 - Planning",
    ],
)
