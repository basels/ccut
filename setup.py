import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ccut",
    version="0.0.1",
    author="Basel Shbita",
    author_email="basel921@gmail.com",
    description="A package for identifying, parsing and transforming units of measure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/basels/ccut/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'arpeggio>=1.9.2',
        'rdflib>=4.2.2'
    ]
)