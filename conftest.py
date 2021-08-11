import json

import pytest

from jina import __version__


def pytest_addoption(parser):
    parser.addoption("--output-file", action="store", default="report.json")


@pytest.fixture(scope='session')
def json_writer(pytestconfig):
    results = []
    yield results

    from pathlib import Path
    output_dir = 'docs/static/artifacts/{}'.format(__version__)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    file_name = pytestconfig.getoption("output_file")
    with open(f'{output_dir}/{file_name}', 'w+') as file:
        json.dump(results, file)
