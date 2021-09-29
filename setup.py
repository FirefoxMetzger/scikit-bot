import setuptools

install_requires = ["numpy == 1.21.2", "scipy == 1.7.1"]

extras_require = {
    "ignition": [
        "pyzmq == 22.3.0",
        "betterproto == 1.2.5",
        "psutil == 5.8.0",
        "requests == 2.26.0",
        "xsdata == 21.9",
        "lxml == 4.6.3",
        "cachetools == 4.2.2",
    ],
    "docs": [
        "sphinx == 4.2.0",
        "numpydoc == 1.1.0",
        "sphinx-autodoc-typehints == 1.12.0",
        "matplotlib == 3.4.3",
        "pydata-sphinx-theme == 0.6.3",
        "cachetools == 4.2.2",
        "sphinx-gallery == 0.10.0",
        "xsdata == 21.9",
        "lxml == 4.6.3",
    ],
    "linting": ["flake8 == 3.9.2", "black == 21.9b0"],
    "testing": ["pytest == 6.2.5", "coverage[toml] == 5.5"],
    "dev": [
        "lxml-stubs == 0.2.0",
        "python-semantic-release == 7.19.2",
    ],
    "build": [
        "build == 0.7.0",
        "twine == 3.4.2",
    ],
}

# Note: This is a shim, because I am used to developing
# under pip install -e . which PEP517 doesn't support (yet?)
if __name__ == "__main__":
    setuptools.setup(
        install_requires=install_requires,
        extras_require=extras_require,
        package_data={"skbot": ["ignition/sdformat/schema/**/*.xsd"]},
    )
