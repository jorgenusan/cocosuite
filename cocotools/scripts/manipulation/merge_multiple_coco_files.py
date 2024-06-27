import json
from pathlib import Path

import fire
from coco_merge import coco_merge
from loguru import logger


def add_ann_folder_to_img_name(ann_file: str) -> str:
    """Add the parent folder to image filenames in annotation file.

    Args:
        ann_file (str): Path to the annotation file.

    Returns:
        str: Path to the modified version of the annotation json file.
    """
    full_path = Path(ann_file)
    parent_folder = full_path.parent.name
    path_to_mod_file = f"{full_path.parent}/{Path(ann_file).stem}_to-merge.json"

    with open(ann_file, "r") as f:
        orig_data = json.load(f)

    for img in orig_data["images"]:
        img["file_name"] = parent_folder + "/" + img["file_name"]

    with open(path_to_mod_file, "w") as f:
        json.dump(orig_data, f, indent=2)

    return path_to_mod_file


def delete_merged_files(files_to_delete: list) -> None:
    """Remove the '*_to-merge.json' files created in the 'add_ann_folder_to_ann_file' method that are no longer needed."""
    for file in files_to_delete:
        Path(file).unlink()
        logger.info(f"{file} deleted.")


def merge_multiple_coco_files(
    dir_path: str,
    output_file: str = "merged_annotations.json",
    name_pattern: str = "*.json",
) -> None:
    """Fetch subdirectories looking for coco annotation files.

    Merge all the coco files inside the dir_path into a single file.

    Args:
        dir_path (str): Parent directory, contains subdirectories with their own annotations and images.
        output_file (str, optional): Name of the file resulting from doing the merge.
        name_pattern (str, optional): Name pattern of the files to merge, leaving those that do not match unmerged.
    """
    coco_files = sorted([str(file) for file in Path(dir_path).rglob(name_pattern)])

    if not coco_files:
        logger.error(f'No files with pattern "{name_pattern}" found in "{dir_path}".')
        exit()

    ann_file_update = add_ann_folder_to_img_name(coco_files[0])
    files_to_delete = [ann_file_update]

    output_path = str(Path(dir_path, output_file))

    for file in coco_files[1:]:
        file_to_add = add_ann_folder_to_img_name(file)

        logger.info(f"Merging {file_to_add} into {ann_file_update}.")
        coco_merge(ann_file_update, file_to_add, output_path)
        ann_file_update = output_path
        files_to_delete.append(file_to_add)

    delete_merged_files(files_to_delete)
    logger.info("Merges done!")


if __name__ == "__main__":
    fire.Fire(merge_multiple_coco_files)
