"""geokiy_py module."""

import io
import os

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()
here = os.path.abspath(os.path.dirname(__file__))

# get the dependencies and installs
with io.open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")
install_requires = [x.strip() for x in all_reqs if "git+" not in x]

# Dev Requirements
extra_reqs = {
    "test": ["pytest", "pytest-cov"],
    "dev": ["pytest", "pytest-cov", "pre-commit"],
}

setup(
    name="geokit_py",
    author="Yunica",
    author_email="junior@developmentseed.org`",
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Python Scripts for geokit",
    url="https://github.com/developmentseed/geokit/tree/develop/py_scripts",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require=extra_reqs,
    entry_points={
        "console_scripts": [
            "chips_ahoy=geokit_py.chips_ahoy.main:cli",
            "cvat=geokit_py.cvat.main:cli",
            "geo=geokit_py.geo.main:cli",
            "rl_schoolspoint=geokit_py.rl_schoolspoint.main:main",
        ],
    },
)
