import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SiteLinks",
    version="0.0.7",
    author="Elly Mandliel",
    author_email="ellykido@google.com",
    description="A link-scanning tool to scrape web urls.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EllyMandliel/SiteLinks",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    requirements=[
      'aiohttp',
      'beautifulsoup4'
    ],
    python_requires='>=3',
)