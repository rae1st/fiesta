from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fiesta-discord",
    version="1.0.0",
    author="fiestapy",
    author_email="dev@fiesta.py",
    description="Modern Discord API wrapper with hybrid commands and built-in interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fiesta-py/fiesta",
    project_urls={
        "Documentation": "https://fiesta-py.readthedocs.io/",
        "Source": "https://github.com/fiesta-py/fiesta",
        "Tracker": "https://github.com/fiesta-py/fiesta/issues",
    },
    packages=find_packages(exclude=("tests", "examples")),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.8,<3.13",
    install_requires=[
        "aiohttp>=3.9.0",
    ],
    extras_require={
        "voice": ["PyNaCl>=1.5.0"],
        "speed": [
            "orjson>=3.8.0",
            "aiodns>=3.0.0",
            "fastchardet>=0.2.0",
        ],
    },
    keywords="discord api bot async hybrid commands interactions",
)
