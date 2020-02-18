try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
setup(
    name='ml scripts',
    version='1.0',
    description='Python scripts for ',
    author='developmentseed',
    packages=find_packages(),
    scripts=[
        'utils.py',
    ],
    entry_points={
        'console_scripts': [
            'juego=cvt_smallbox.command_line:main',

        ],
    }
)
