from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="census-cb",
    version="0.1.0",
    author="Tim Crammond",
    author_email="author@example.com",
    description="Wrapper for downloading and processing Cartography Boundaries from the US Census Bureau",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tcramm0nd/census-cb",
    project_urls={
        "Bug Tracker": "https://github.com/tcramm0nd/census-cb/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['geopandas==0.9.0',
                      'pandas==1.3.2',
                      'requests==2.26.0']
)