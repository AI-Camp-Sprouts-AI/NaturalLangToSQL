import pytest


def pytest_addoption(parser):
    parser.addoption("--test_suite", action="store",
                     default="default website_aggregates")

# assertion_count = 0

# def pytest_assertion_pass(item, lineno, orig, expl):
#     global assertion_count
#     assertion_count += 1

# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     print(f'{assertion_count} assertions tested.')

@pytest.fixture
def test_suite(request):
    return request.config.getoption("--test_suite")
