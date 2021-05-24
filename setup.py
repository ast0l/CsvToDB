import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csvtodb",
    version="1.1.1",
    author="akk0ga",
    author_email="ttn.glock@orange.fr",
    description="Make it easier to build database/table/seeders for DBMS or framework like laravel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akk0ga/CsvToDB",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=setuptools.find_packages(),
    keywords=['csv', 'db', 'database', 'sql', 'framework', 'mysql'],
    python_requires=">=3.6",
)
