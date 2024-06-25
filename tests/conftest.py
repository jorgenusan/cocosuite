from pathlib import Path

import pytest


@pytest.fixture
def project_root_path(request):
    return Path(request.config.rootpath)
