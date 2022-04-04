#!/usr/bin/env python
import sys
import django


def main():
    print(
        "\n\n\n%s\n Python: %s, Django: %s\n%s\n"
        % (
            "=" * 120,
            ".".join(map(str, sys.version_info[:3])),
            ".".join(map(str, django.VERSION[:3])),
            "-" * 120,
        )
    )

    import logging

    logging.basicConfig(level=logging.ERROR)

    from conftest import pytest_configure

    settings = pytest_configure()

    from django.test.utils import get_runner

    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    original_suite_result = test_runner.suite_result

    def patched_suite_result(suite, result, **kwargs):
        from formapi.tests import TOTAL_TESTS

        assert result.testsRun == TOTAL_TESTS, "Run {} tests, expected to run {}".format(
            result.testsRun,
            TOTAL_TESTS,
        )
        return original_suite_result(suite, result, **kwargs)

    test_runner.suite_result = patched_suite_result

    failures = test_runner.run_tests(["formapi"])
    sys.exit(failures)


if __name__ == "__main__":
    main()
