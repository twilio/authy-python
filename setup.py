from authy import __version__
from setuptools import setup, find_packages

# to install authy type the following command: 
#     python setup.py install 
#

setup(
    name = "authy",
    version = __version__,
    description = "Authy API Client",
    author = "Authy Inc",
    author_email = "help@authy.com",
    url = "http://github.com/authy/python-authy",
    keywords = ["authy"],
    install_requires = ["httplib2 >= 0.7, < 0.8", "simplejson"],
    packages = find_packages(),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security"
        ],
    long_description = """\
    Authy API Client for Python
""" )
