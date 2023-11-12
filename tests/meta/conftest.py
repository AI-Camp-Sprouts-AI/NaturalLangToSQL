import pytest


def pytest_addoption(parser):
    parser.addoption("--test_suite", action="store",
                     default="default website_aggregates")


@pytest.fixture
def test_suite(request):
    return request.config.getoption("--test_suite")
