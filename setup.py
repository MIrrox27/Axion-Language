# author https://github.com/MIrrox27/Axion-Language
# setup.py


from setuptools import setup, find_packages
from axion import __version__

with open("README.md", 'r', encoding="utf-8") as fh:
    long_description = fh.read()

import re
with open("axion/__init__.py", "r", encoding="utf-8") as f:
    version_match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", f.read())
    __version__ = version_match.group(1) if version_match else __version__



setup(
    name="axion",
    version=__version__,
    description="Axion Programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Maksim Pronkin",
    author_email="maksim.pronkin@gmail.com",
    url="https://github.com/MIrrox27/Axion-Language",

    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "axion = axion.__main__:main",
        ],
    },

    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[],
)