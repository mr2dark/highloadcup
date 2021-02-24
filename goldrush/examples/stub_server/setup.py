# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "openapi_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="HighLoad Cup 2021",
    author_email="",
    url="",
    keywords=["OpenAPI", "HighLoad Cup 2021"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description="""\
    ## Usage ## List of all custom errors First number is HTTP Status code, second is value of \&quot;code\&quot; field in returned JSON object, text description may or may not match \&quot;message\&quot; field in returned JSON object. - 422.1000: wrong coordinates - 422.1001: wrong depth - 409.1002: no more active licenses allowed - 409.1003: treasure is not digged 
    """
)

