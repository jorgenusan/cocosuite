import json
import tempfile
from pathlib import Path

import pytest

from cocotoolkit.scripts.manipulation.random_split import random_split


@pytest.mark.parametrize(
    "input_json",
    [
        "coco_example_1.json",
        "coco_example_2.json",
    ],
)
def test_random_split_output_files(input_json, project_root_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        input_json_path = project_root_path / "examples" / input_json
        output_file = Path(temp_dir) / "random_split_output"

        random_split(
            str(input_json_path), str(output_file), train_percentage=0.8, seed=47
        )

        assert Path(f"{output_file}_train.json").exists()
        assert Path(f"{output_file}_val.json").exists()


@pytest.mark.parametrize(
    "input_json, train_percentage",
    [
        ("coco_example_1.json", 0.7),
        ("coco_example_2.json", 0.9),
    ],
)
def test_random_split_proportions(input_json, train_percentage, project_root_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        input_json_path = project_root_path / "examples" / input_json
        output_file = Path(temp_dir) / "random_split_output"

        random_split(
            str(input_json_path),
            str(output_file),
            train_percentage=train_percentage,
            seed=47,
        )

        with open(f"{output_file}_train.json", "r") as f:
            train_json = json.load(f)
        with open(f"{output_file}_val.json", "r") as f:
            val_json = json.load(f)

        train_proportion = len(train_json["images"]) / (
            len(train_json["images"]) + len(val_json["images"])
        )
        val_proportion = len(val_json["images"]) / (
            len(train_json["images"]) + len(val_json["images"])
        )

        assert abs(train_proportion - train_percentage) < 0.01
        assert abs(val_proportion - (1 - train_percentage)) < 0.01


@pytest.mark.parametrize(
    "input_json, train_percentage, seed",
    [
        ("coco_example_1.json", 0.7, 47),
        ("coco_example_2.json", 0.9, 23),
    ],
)
def test_random_split_coco_format(
    input_json, train_percentage, seed, project_root_path
):
    with tempfile.TemporaryDirectory() as temp_dir:
        input_json_path = project_root_path / "examples" / input_json
        output_file = Path(temp_dir) / "random_split_output"

        random_split(str(input_json_path), str(output_file), train_percentage, seed)

        with open(f"{output_file}_train.json", "r") as f:
            train_data = json.load(f)
        with open(f"{output_file}_val.json", "r") as f:
            val_data = json.load(f)

        necessary_keys = ["info", "licenses", "images", "annotations", "categories"]
        for key in necessary_keys:
            assert key in train_data
            assert key in val_data
