import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CsvToDB",
    version="0.0.1",
    author="akk0ga",
    author_email="ttn.glock@orange.fr",
    description="Make it easier to build database/table/seeders for DBMS or web framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/akk0ga/csv_parser",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['CsvToDB'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
