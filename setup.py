import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cegal-welltools",
    version="0.1.0",
    author="Hilde Haland",
    author_email="hilde.tveit.haland@gmail.com",
    description="Cegal AS-provided well log package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cegaldev/cegaltools",
    packages=setuptools.find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    install_requires=[
        "colour>=0.1.5",
        "scikit-learn>=0.22.1",
        "lasio>=0.25.1",
        "pandas>=1.0.3",
        "plotly>=4.6.0",
        "numpy>=1.18.0"
    ]
)
