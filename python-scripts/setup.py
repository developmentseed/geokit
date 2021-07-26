from setuptools import find_packages, setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='geokit_py',
    author="Yunica",
    author_email="junior@developmentseed.org`",
    version='0.0.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="",
    url="https://github.com/developmentseed/geokit/tree/develop/py_scripts",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cvat=geokit_py.cvat.main:cli',
            'geo=geokit_py.geo.main:cli',

            'rl_schoolspoint=geokit_py.rl_schoolspoint.__init__:main',
        ],
    },
)
