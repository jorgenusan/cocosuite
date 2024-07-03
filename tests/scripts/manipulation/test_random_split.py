import json
import tempfile
from pathlib import Path

import pytest

from cocosuite.scripts.manipulation.random_split import random_split


def test_random_split_output_files(sample_data):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file = temp_dir_path / "sample_data.json"
        temp_file.write_text(json.dumps(sample_data))

        output_file = temp_dir_path / "random_split_output"

        random_split(str(temp_file), str(output_file), train_percentage=0.8, seed=47)

        assert Path(f"{output_file}_train.json").exists()
        assert Path(f"{output_file}_val.json").exists()


@pytest.mark.parametrize(
    "train_percentage",
    [
        0.7,
        0.9,
    ],
)
def test_random_split_proportions(train_percentage, sample_data):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file = temp_dir_path / "sample_data.json"
        temp_file.write_text(json.dumps(sample_data))
        output_file = temp_dir_path / "random_split_output"

        random_split(
            str(temp_file),
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
    "train_percentage, seed",
    [
        (0.7, 47),
        (0.9, 23),
    ],
)
def test_random_split_coco_format(train_percentage, seed, sample_data):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file = temp_dir_path / "sample_data.json"
        temp_file.write_text(json.dumps(sample_data))
        output_file = temp_dir_path / "random_split_output"

        random_split(str(temp_file), str(output_file), train_percentage, seed)

        with open(f"{output_file}_train.json", "r") as f:
            train_data = json.load(f)
        with open(f"{output_file}_val.json", "r") as f:
            val_data = json.load(f)

        necessary_keys = ["info", "licenses", "images", "annotations", "categories"]
        for key in necessary_keys:
            assert key in train_data
            assert key in val_data
