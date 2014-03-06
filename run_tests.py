#!/usr/bin/env python
# coding=utf-8
import sys


def main():
    from conftest import pytest_configure
    settings = pytest_configure()

    from django.test.utils import get_runner

    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['formapi'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
