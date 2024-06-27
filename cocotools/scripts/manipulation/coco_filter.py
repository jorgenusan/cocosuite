import json
from pathlib import Path

import fire
from loguru import logger


def filter_annotations(
    annotations_file: str,
    filter_config_file: str,
    output_filename: str = "filtered_annotations.json",
):
    """Filter the input json file based on the filter criteria.

    Args:
        annotations_file (str): JSON file containing COCO formatted data.
        filter_config_file (str): JSON file containing the criteria for filtering the data.
        output_filename (Optional[str], optional): Name of the output json file. Defaults to "filtered_annotations.json".
        output_path (Optional[str], optional): Path to save the output file. Defaults to None.
    """
    with open(annotations_file, "r") as f:
        coco_data = json.load(f)

    with open(filter_config_file, "r") as f:
        filter_config = json.load(f)
    filters = filter_config["filter"]
    match_all = filter_config.get("match_all", False)

    logger.info(f"Filtering data based on the criteria: {filters}")
    filtered_images = []
    filtered_annotations = []

    for image in coco_data["images"]:
        if match_all:
            match = all(
                key in image and any(str(value) in str(image[key]) for value in values)
                for key, values in filters.items()
            )
        else:
            match = any(
                key in image and any(str(value) in str(image[key]) for value in values)
                for key, values in filters.items()
            )

        if not match:
            filtered_images.append(image)
            filtered_annotations.extend(
                [
                    ann
                    for ann in coco_data["annotations"]
                    if ann["image_id"] == image["id"]
                ]
            )

    filtered_data = {
        "info": coco_data.get("info", {}),
        "licenses": coco_data.get("licenses", []),
        "images": filtered_images,
        "annotations": filtered_annotations,
        "categories": coco_data["categories"],
    }

    if len(output_filename.rsplit("/", 1)) >= 2:
        file_path = Path(output_filename).parent
    else:
        file_path = Path(annotations_file).parent

    output_file = Path(file_path, output_filename)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved filtered data into {output_filename}")


if __name__ == "__main__":
    fire.Fire(filter_annotations)
