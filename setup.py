from setuptools import find_packages, setup

import os


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name="boj-checker",
    version=get_version("src/boj_checker/__init__.py"),
    description="Test BOJ solution using sample IOs.",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
    url="https://github.com/sohnryang/boj-checker",
    project_urls={"Source": "https://github.com/sohnryang/boj-checker"},
    author="Ryang Sohn",
    author_email="loop.infinitely@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={"console_scripts": ["boj-checker=boj_checker:entry"]},
    python_requires=">=3.7",
    install_requires=["requests", "colorama", "beautifulsoup4", "xdg"],
    zip_safe=False,
)
