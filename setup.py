import setuptools

# install src dir
setuptools.setup(
    name="src",
    version="0.0.0",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
)
