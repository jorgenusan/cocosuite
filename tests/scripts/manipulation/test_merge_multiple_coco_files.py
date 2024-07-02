from pathlib import Path
from tempfile import TemporaryDirectory

from cocosuite.scripts.manipulation.merge_multiple_coco_files import (
    add_ann_folder_to_img_name,
    delete_merged_files,
    merge_multiple_coco_files,
)
from tests.conftest import load_json_file


def test_merge_multiple_coco_files_integration(project_root_path):
    example_files = [
        project_root_path / "examples/coco_example_1.json",
        project_root_path / "examples/coco_example_2.json",
    ]

    with TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        for i, example_file in enumerate(example_files):
            temp_file = temp_dir_path / f"example_{i+1}.json"
            temp_file.write_text(example_file.read_text())

        merge_multiple_coco_files(
            str(temp_dir_path),
            output_file="merged_annotations.json",
            name_pattern="*.json",
        )

        result_file = temp_dir_path / "merged_annotations.json"
        assert result_file.exists()

        merged_data = load_json_file(result_file)
        expected_num_images = sum(
            len(load_json_file(file)["images"]) for file in example_files
        )
        expected_num_annotations = sum(
            len(load_json_file(file)["annotations"]) for file in example_files
        )
        unique_categories = set()
        for file in example_files:
            data = load_json_file(file)
            unique_categories.update(
                category["name"] for category in data["categories"]
            )

        assert len(merged_data["images"]) == expected_num_images
        assert len(merged_data["annotations"]) == expected_num_annotations
        assert len(merged_data["categories"]) == len(unique_categories)


def test_add_ann_folder_to_img_name(project_root_path):
    example_file = project_root_path / "examples/coco_example_1.json"

    with TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir) / "example.json"
        temp_file.write_text(example_file.read_text())

        updated_file = add_ann_folder_to_img_name(str(temp_file))
        updated_data = load_json_file(updated_file)

        parent_folder = Path(temp_file).parent.name
        for img in updated_data["images"]:
            assert img["file_name"].startswith(f"{parent_folder}/")


def test_delete_merged_files(project_root_path):
    with TemporaryDirectory() as temp_dir:
        example_files = [
            project_root_path / "examples/coco_example_1.json",
            project_root_path / "examples/coco_example_2.json",
        ]

        temp_files = []
        for i, example_file in enumerate(example_files):
            temp_file = Path(temp_dir) / f"example_{i+1}.json"
            temp_file.write_text(example_file.read_text())
            temp_files.append(str(temp_file))

        delete_merged_files(temp_files)

        for temp_file in temp_files:
            assert not Path(temp_file).exists()
