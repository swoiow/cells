from distutils.core import setup

from setuptools import find_packages

setup(
    name="cells",
    version="0.0.3",
    url="",
    license="MPL-2.0",
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
        "colorama",
    ]
)
