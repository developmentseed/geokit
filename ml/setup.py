try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
setup(
    name='ml scripts',
    version='1.0',
    description='Python scripts for ml data cleared ',
    author='developmentseed',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cvat_smallbox=cvat_smallbox.command_line:main'
        ],
    },
)
