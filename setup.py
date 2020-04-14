from authy import __version__
from setuptools import setup, find_packages

# to install authy type the following command:
#     python setup.py install

with open('README.md') as f:
    long_description = f.read()

setup(
    name="authy",
    version=__version__,
    description="Authy API Client",
    author="Authy Inc",
    author_email="dev-support@authy.com",
    url="http://github.com/authy/authy-python",
    keywords=["authy", "two factor", "authentication"],
    install_requires=[
        "requests>=2.2.1",
        "six>=1.8.0",
        "simplejson>=3.4.0;python_version<'2.6'",
    ],
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
