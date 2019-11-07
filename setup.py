import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xtabular", # Replace with your own username
    version="0.0.1",
    author="Manuel Pfeuffer",
    author_email="manuel.pfeuffer@hu-berlin.de",
    description="A small package to colorize LaTeX tables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mpff/xtabular",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)
