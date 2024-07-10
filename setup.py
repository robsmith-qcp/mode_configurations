# setup.py

from setuptools import setup, find_packages

setup(
    name="mode_configurations",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pytest",
        "scipy",
    ],
    author="Robert Smith",
    author_email="robs84@vt.edu",
    description="A package for generating geometric configurations accounting for zero-point motion",
    url="https://github.com/robsmith-qcp/mode_configurations.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

