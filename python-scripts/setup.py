"""geokiy_py module."""

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

# Dev Requirements
extra_reqs = {
    "test": ["pytest", "pytest-cov"],
    "dev": ["pytest", "pytest-cov", "pre-commit"],
}
inst_reqs = ["click"]


setup(
    name="geokit_py",
    author="Yunica",
    author_email="junior@developmentseed.org`",
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="",
    url="https://github.com/developmentseed/geokit/tree/develop/py_scripts",
    packages=find_packages(),
    install_requires=inst_reqs,
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