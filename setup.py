from setuptools import find_packages, setup

# Declaring variables for setup functions
PROJECT_NAME = "Face Authenticator"
VERSION = "0.0.0"
AUTHOR = "Sunitha LV"
DESCRIPTION = "This is a Face Authenticator Project"


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
)
