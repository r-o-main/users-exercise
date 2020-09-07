import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ricardo-users-exercise",
    version="0.0.1",
    author="Romain Bouteloup",
    author_email="romain.bouteloup@gmail.com",
    description="A simple REST API users package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/r-o-main/users-exercise",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'django',
        'djangorestframework',
        'markdown',
        'pylint_django',
        'coverage',
        'django-filter',
        'ipapi',
        'kafka-python',
        'pyyaml',
        'termcolor',
      ],
)