#!/usr/bin/env python
# coding=utf-8

import codecs
import os
import sys
from setuptools import setup, find_packages

import formapi

readme = os.path.join(os.path.dirname(__file__), "README.rst")
readme = codecs.open(readme).read()
if (3, 3) <= sys.version_info < (3, 4, 3):
    readme = readme.decode("utf8")

setup(
    name="django-formapi",
    version=formapi.__version__,
    description="Django API creation with signed requests utilizing forms for validation.",
    long_description=readme,
    author="Hannes Ljungberg",
    author_email="hannes@5monkeys.se",
    url="http://github.com/5monkeys/django-formapi",
    download_url="https://github.com/5monkeys/django-formapi/tarball/%s"
    % (formapi.__version__,),
    keywords=[
        "django",
        "formapi",
        "api",
        "rpc",
        "signed",
        "request",
        "form",
        "validation",
    ],
    platforms=["any"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Framework :: Django",
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    tests_require=["Django", "pytz", "importlib"],
    test_suite="run_tests.main",
)
