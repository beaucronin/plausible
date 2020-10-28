import os

from setuptools import setup, find_packages

# Meta information
version = open("VERSION").read().strip()
dirname = os.path.dirname(__file__)

setup(
    # Basic info
    name="plausible_cli",
    version=version,
    author="Beau Cronin",
    author_email="beau.cronin@gmail.com",
    url="https://github.com/beaucronin/plausible",
    description="Command line interface for Plausible",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    # Packages and depencies
    # package_dir={'': 'plausible_cli'},
    packages=find_packages(''),
    include_package_date=True,
    install_requires=[
        "colorama",
        "python-terraform",
        "shellingham",
        "typer",
        "git+https://github.com/beaucronin/strictyaml",
    ],
    # Scripts
    entry_points={
        'console_scripts': [
            'pls = plausible_cli.main:app'],
    },
    # Other configurations
    zip_safe=False,
    platforms="any",
)
