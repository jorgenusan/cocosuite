import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cocosuite.scripts.manipulation.property_split import property_split


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
