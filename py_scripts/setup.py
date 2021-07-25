try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages



setup(
    name='geokit_py',
    version='1.0',
    description='Python scripts for geokit ',
    author='developmentseed',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cvat_smallbox=src.cvat_smallbox.__init__:main',
            'cvat_intersectionbox=src.cvat_intersectionbox.__init__:main',
            'rl_schoolspoint=src.rl_schoolspoint.__init__:main',

            'geo_generateid=src.geo_generateid.__init__:main',

        ],
    },
)
