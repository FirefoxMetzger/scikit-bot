import setuptools

install_requires = ["numpy == 1.21.1", "scipy == 1.7.0"]

extras_require = {
    "ignition": ["pyzmq == 22.1.0", "betterproto == 1.2.5", "psutil == 5.8.0"],
    "docs": [
        "sphinx == 4.1.1",
        "numpydoc == 1.1.0",
        "sphinx-autodoc-typehints == 1.12.0",
        "matplotlib == 3.4.2",
        "pydata-sphinx-theme == 0.6.3",
    ],
    "linting": ["flake8 == 3.9.2", "black == 21.7b0"],
    "testing": ["pytest == 6.2.4", "coverage[toml] == 5.5"],
}

# Note: This is a shim, because I am used to developing
# under pip install -e . which PEP517 doesn't support (yet?)
if __name__ == "__main__":
    setuptools.setup(install_requires=install_requires, extras_require=extras_require)
