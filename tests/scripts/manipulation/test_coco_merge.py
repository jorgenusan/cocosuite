import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cocosuite.scripts.manipulation.coco_merge import coco_merge


def prepare_and_merge_coco_files(data1: dict, data2: dict, temp_dir: Path) -> dict:
    coco_1 = temp_dir / "coco_1.json"
    coco_2 = temp_dir / "coco_2.json"
    with open(coco_1, "w") as f:
        json.dump(data1, f)
    with open(coco_2, "w") as f:
        json.dump(data2, f)

    result_file = coco_merge(str(coco_1), str(coco_2))
    assert Path(result_file).exists()

    with open(result_file, "r") as f:
        return json.load(f)


def test_coco_merge_with_example_files(sample_data: dict):
    data1 = copy.deepcopy(sample_data)
    data2 = copy.deepcopy(sample_data)
    data2["categories"][1]["name"] = "cat3"

    expected_num_images = len(data1.get("images", [])) * 2
    expected_num_annotations = len(data1.get("annotations", [])) * 2
    expected_num_categories = len(data1.get("categories", [])) + 1

    with TemporaryDirectory() as temp_dir:
        merged_data = prepare_and_merge_coco_files(data1, data2, Path(temp_dir))

        assert len(merged_data["images"]) == expected_num_images
        assert len(merged_data["annotations"]) == expected_num_annotations
        assert len(merged_data["categories"]) == expected_num_categories


def test_coco_merge_with_empty_file(sample_data: dict, empty_sample_data: dict):
    data = copy.deepcopy(sample_data)

    expected_num_images = len(data.get("images", []))
    expected_num_annotations = len(data.get("annotations", []))
    expected_num_categories = len(data.get("categories", []))

    with TemporaryDirectory() as temp_dir:
        merged_data = prepare_and_merge_coco_files(
            data, empty_sample_data, Path(temp_dir)
        )

        assert len(merged_data["images"]) == expected_num_images
        assert len(merged_data["annotations"]) == expected_num_annotations
        assert len(merged_data["categories"]) == expected_num_categories
