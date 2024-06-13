from setuptools import setup, find_packages

setup(
    name="substack_md_parser",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Meet Gor",
    author_email="gormeet711@gmail.com",
    description="A parser for Substack and Markdown",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mr-destructive/substack-md-parser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
