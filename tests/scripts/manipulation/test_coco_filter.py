import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cocosuite.scripts.manipulation.coco_filter import filter_annotations


def run_filter_annotations_test(sample_data, sample_config, match_all=True):
    with TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "coco_data.json"
        with open(temp_file, "w") as f:
            json.dump(sample_data, f)

        sample_config["match_all"] = match_all
        filter_config_file = Path(temp_dir) / "filter_config.json"
        with open(filter_config_file, "w") as f:
            json.dump(sample_config, f)

        output_file = Path(temp_dir) / "filtered_annotations.json"
        filter_annotations(str(temp_file), str(filter_config_file), str(output_file))

        assert output_file.exists()

        with open(output_file, "r") as f:
            return json.load(f)


def test_filter_annotations_match_all(sample_data, sample_config):
    filtered_data = run_filter_annotations_test(
        sample_data, sample_config, match_all=True
    )

    expected_filtered_images = sample_data["images"][1:]
    expected_filtered_annotations = sample_data["annotations"][1:]

    assert filtered_data["images"] == expected_filtered_images
    assert filtered_data["annotations"] == expected_filtered_annotations


def test_filter_annotations_match_any(sample_data, sample_config):
    filtered_data = run_filter_annotations_test(
        sample_data, sample_config, match_all=False
    )

    expected_filtered_images = sample_data["images"][5:]
    expected_filtered_annotations = sample_data["annotations"][5:]

    assert filtered_data["images"] == expected_filtered_images
    assert filtered_data["annotations"] == expected_filtered_annotations
