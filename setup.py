import os
import sys

from reflect.version import VERSION

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = [
    'jwcrypto>=0.4.2,<0.5'
]

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'reflect'))

setup(
    name='reflect',
    cmdclass={'build_py': build_py},
    version=VERSION,
    description='Reflect Python bindings',
    long_description="A Python wrapper for the Reflect API.",
    author='Reflect',
    author_email='support@reflect.io',
    url='https://github.com/reflect/reflect-python',
    packages=['reflect'],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
