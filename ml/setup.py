try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
setup(
    scripts = [
        'cvt_smallbox.py'
    ]
)