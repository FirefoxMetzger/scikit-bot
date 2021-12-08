import setuptools

install_requires = ["numpy == 1.21.4", "scipy == 1.7.3"]

extras_require = {
    "ignition": [
        "pyzmq == 22.3.0",
        "betterproto == 1.2.5",
        "psutil == 5.8.0",
        "requests == 2.26.0",
        "xsdata == 21.12",
        "lxml == 4.6.4",
        "cachetools == 4.2.4",
    ],
    "docs": [
        "sphinx == 4.3.1",
        "numpydoc == 1.1.0",
        "sphinx-autodoc-typehints == 1.12.0",
        "matplotlib == 3.5.0",
        "pydata-sphinx-theme == 0.7.2",
        "cachetools == 4.2.4",
        "sphinx-gallery == 0.10.1",
        "xsdata == 21.12",
        "lxml == 4.6.4",
    ],
    "linting": ["flake8 == 4.0.1", "black == 21.12b0"],
    "testing": ["pytest == 6.2.5", "coverage[toml] == 6.2"],
    "dev": [
        "lxml-stubs == 0.3.0",
        "python-semantic-release == 7.23.0",
    ],
    "build": [
        "build == 0.7.0",
        "twine == 3.7.1",
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
