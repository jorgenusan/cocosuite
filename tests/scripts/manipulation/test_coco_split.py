import json
import tempfile
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from cocosuite.scripts.manipulation.coco_split import property_split, random_split


def run_property_split_test(sample_data, sample_config):
    with TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "coco_data.json"
        with open(temp_file, "w") as f:
            json.dump(sample_data, f)

        split_config_file = Path(temp_dir) / "split_config.json"
        with open(split_config_file, "w") as f:
            json.dump(sample_config, f)

        output_file = Path(temp_dir) / "property_split.json"
        property_split(str(temp_file), str(split_config_file), str(output_file))

        train_output_file = Path(temp_dir) / "property_split_train.json"
        val_output_file = Path(temp_dir) / "property_split_val.json"

        assert train_output_file.exists()
        assert val_output_file.exists()

        with open(train_output_file, "r") as f:
            train_data = json.load(f)
        with open(val_output_file, "r") as f:
            val_data = json.load(f)

        return train_data, val_data


def test_property_split_match_all(sample_data, sample_config):
    train_data, val_data = run_property_split_test(sample_data, sample_config)

    expected_train_images = sample_data["images"][1:]
    expected_train_annotations = sample_data["annotations"][1:]
    expected_val_images = [sample_data["images"][0]]
    expected_val_annotations = [sample_data["annotations"][0]]

    assert train_data["images"] == expected_train_images
    assert train_data["annotations"] == expected_train_annotations
    assert val_data["images"] == expected_val_images
    assert val_data["annotations"] == expected_val_annotations


def test_property_split_match_any(sample_data, sample_config):
    sample_config["match_all"] = False
    train_data, val_data = run_property_split_test(sample_data, sample_config)

    expected_train_images = sample_data["images"][5:]
    expected_train_annotations = sample_data["annotations"][5:]
    expected_val_images = sample_data["images"][:5]
    expected_val_annotations = sample_data["annotations"][:5]

    assert train_data["images"] == expected_train_images
    assert train_data["annotations"] == expected_train_annotations
    assert val_data["images"] == expected_val_images
    assert val_data["annotations"] == expected_val_annotations


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
