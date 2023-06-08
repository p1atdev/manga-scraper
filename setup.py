from setuptools import setup, find_packages


setup(
    name="manga-scraper",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "feedparser",
        "opencv-python",
        "python-opencv-utils",
        "tqdm",
        "numpy",
        "requests",
    ],
)
