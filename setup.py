import re

from setuptools import setup


def get_version(filename):
    with open(filename, "r") as fp:
        contents = fp.read()
    return re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents).group(1)


version = get_version("flake8_comprehensions.py")


with open("README.rst", "r") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", "r") as history_file:
    history = history_file.read()

setup(
    name="flake8-comprehensions",
    version=version,
    description="A flake8 plugin to help you write better list/set/dict "
    "comprehensions.",
    long_description=readme + "\n\n" + history,
    author="Adam Johnson",
    author_email="me@adamj.eu",
    url="https://github.com/adamchainz/flake8-comprehensions",
    project_urls={
        "Changelog": (
            "https://github.com/adamchainz/flake8-comprehensions"
            + "/blob/master/HISTORY.rst"
        )
    },
    entry_points={
        "flake8.extension": ["C4 = flake8_comprehensions:ComprehensionChecker"]
    },
    py_modules=["flake8_comprehensions"],
    include_package_data=True,
    install_requires=["flake8!=3.2.0"],
    python_requires=">=3.5",
    license="ISCL",
    zip_safe=False,
    keywords="flake8, comprehensions, list comprehension, set comprehension, "
    "dict comprehension",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
