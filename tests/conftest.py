import json
from pathlib import Path

import pytest


@pytest.fixture
def project_root_path(request):
    return Path(request.config.rootpath)


def load_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
