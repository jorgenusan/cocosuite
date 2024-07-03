import pytest


@pytest.fixture
def sample_data():
    return {
        "info": {
            "description": "example",
            "version": "1.0",
            "year": 2023,
            "contributor": "example contributor",
        },
        "licenses": [
            {"id": 1, "name": "example license", "url": "http://example.com/license"}
        ],
        "images": [
            {"id": 1, "file_name": "image1.jpg", "width": 800, "height": 600},
            {"id": 2, "file_name": "image2.jpg", "width": 800, "height": 600},
            {"id": 3, "file_name": "image3.jpg", "width": 1024, "height": 768},
            {"id": 4, "file_name": "image4.jpg", "width": 1024, "height": 768},
            {"id": 5, "file_name": "image5.jpg", "width": 1024, "height": 768},
            {"id": 6, "file_name": "image6.jpg", "width": 640, "height": 480},
            {"id": 7, "file_name": "image7.jpg", "width": 640, "height": 480},
            {"id": 8, "file_name": "image8.jpg", "width": 640, "height": 480},
            {"id": 9, "file_name": "image9.jpg", "width": 640, "height": 480},
            {"id": 10, "file_name": "imageX.jpg", "width": 640, "height": 480},
        ],
        "annotations": [
            {"id": 1, "image_id": 1, "category_id": 1},
            {"id": 2, "image_id": 2, "category_id": 2},
            {"id": 3, "image_id": 3, "category_id": 1},
            {"id": 4, "image_id": 4, "category_id": 2},
            {"id": 5, "image_id": 5, "category_id": 1},
            {"id": 6, "image_id": 6, "category_id": 2},
            {"id": 7, "image_id": 7, "category_id": 1},
            {"id": 8, "image_id": 8, "category_id": 2},
            {"id": 9, "image_id": 9, "category_id": 1},
            {"id": 10, "image_id": 10, "category_id": 2},
        ],
        "categories": [
            {"id": 1, "name": "cat1"},
            {"id": 2, "name": "cat2"},
        ],
    }


@pytest.fixture
def empty_sample_data():
    return {
        "info": {},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": [],
    }


@pytest.fixture
def sample_config():
    return {
        "criteria": {"file_name": ["image1"], "width": [800, 1024]},
        "filter": {"file_name": ["image1"], "width": [800, 1024]},
        "match_all": True,
    }
