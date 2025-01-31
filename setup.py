from setuptools import setup, find_packages

setup(
    name="iota-python",
    version="0.0.59",
    author="Dr. Brandon Wiley",
    author_email="brandon@blanu.net",
    description="iota-python is the base for python-based implementations and tools for iota",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/blanu/iota-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    install_requires=[
        "testify>=0.11.3",
    ],
)
