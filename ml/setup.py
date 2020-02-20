try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
setup(
    name='ml',
    version='1.0',
    description='Python scripts for ml data cleared ',
    author='developmentseed',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cvat_smallbox=ml_script.cvat_smallbox.command_line:main',
            'cvat_intersectionbox=ml_script.cvat_intersectionbox.command_line:main',

        ],
    },
)
