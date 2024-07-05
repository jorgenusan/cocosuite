import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cocosuite.scripts.manipulation.merge_multiple_coco_files import (
    add_ann_folder_to_img_name,
    delete_merged_files,
    merge_multiple_coco_files,
)


def test_merge_multiple_coco_files_integration_with_fixture(sample_data):
    with TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        temp_file = temp_dir_path / "sample_data.json"
        temp_file.write_text(json.dumps(sample_data))

        temp_file_2 = temp_dir_path / "sample_data_2.json"
        temp_file_2.write_text(json.dumps(sample_data))

        merge_multiple_coco_files(
            str(temp_dir_path),
            output_file="merged_annotations.json",
            name_pattern="*.json",
        )

        result_file = temp_dir_path / "merged_annotations.json"
        assert result_file.exists()

        with open(result_file, "r") as f:
            merged_data = json.load(f)

        expected_num_images = len(sample_data["images"]) * 2
        expected_num_annotations = len(sample_data["annotations"]) * 2
        unique_categories = {cat["name"] for cat in sample_data["categories"]}

        assert len(merged_data["images"]) == expected_num_images
        assert len(merged_data["annotations"]) == expected_num_annotations
        assert len(merged_data["categories"]) == len(unique_categories)


def test_add_ann_folder_to_img_name(sample_data):
    with TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "example.json"
        temp_file.write_text(json.dumps(sample_data))

        updated_file = add_ann_folder_to_img_name(str(temp_file))

        with open(updated_file, "r") as f:
            updated_data = json.load(f)

        parent_folder = Path(temp_file).parent.name
        for img in updated_data["images"]:
            assert img["file_name"].startswith(f"{parent_folder}/")


def test_delete_merged_files(sample_data):
    with TemporaryDirectory() as temp_dir:
        temp_files = []
        for i in range(2):
            temp_file = Path(temp_dir) / f"example_{i + 1}.json"
            temp_file.write_text(json.dumps(sample_data))
            temp_files.append(str(temp_file))

        delete_merged_files(temp_files)

        for temp_file in temp_files:
            assert not Path(temp_file).exists()
