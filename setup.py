from distutils.core import setup

from setuptools import find_packages

setup(
    name="cells",
    version="0.0.1",
    url="",
    license="MIT",
    author="",
    author_email="",
    description="",

    package_dir={},
    packages=find_packages(exclude=["pyext", "*tests.*"]),
    # include_package_data=True,
    platforms="any",
    # ext_package="cells",
    # use_2to3=True,
    install_requires=[
        "six",
    ]
)
