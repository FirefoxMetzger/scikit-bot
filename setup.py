import setuptools

install_requires = ["numpy == 1.21.5", "scipy == 1.7.3", "numba == 0.55.1"]

extras_require = {
    "ignition": [
        "pyzmq == 22.3.0",
        "betterproto == 1.2.5",
        "psutil == 5.9.0",
        "requests == 2.27.1",
        "xsdata == 22.1",
        "lxml == 4.6.5",
        "cachetools == 5.0.0",
    ],
    "docs": [
        "sphinx == 4.4.0",
        "numpydoc == 1.2",
        "sphinx-autodoc-typehints == 1.17.0",
        "matplotlib == 3.5.1",
        "pydata-sphinx-theme == 0.8.0",
        "cachetools == 5.0.0",
        "sphinx-gallery == 0.10.1",
        "xsdata == 22.1",
        "lxml == 4.6.5",
    ],
    "linting": ["flake8 == 4.0.1", "black == 21.12b0"],
    "testing": ["pytest == 7.0.1", "coverage[toml] == 6.3.2"],
    "dev": [
        "lxml-stubs == 0.3.1",
        "python-semantic-release == 7.25.2",
    ],
    "build": [
        "build == 0.7.0",
        "twine == 3.8.0",
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
