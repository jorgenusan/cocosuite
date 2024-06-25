import json

from loguru import logger


def property_split(annotations_file: str, output_filename: str, config_split: str):
    """Split the input json file into train and val json files based on the property criteria.

    Args:
        annotations_file (str): JSON file containing COCO formatted data.
        output_filename (str): Prefix of the output json files.
        config_split (str): JSON file containing the criteria for splitting the data.
    """
    with open(annotations_file, "r") as f:
        coco_data = json.load(f)

    with open(config_split, "r") as f:
        config_data = json.load(f)
    criteria = config_data["criteria"]
    match_all = config_data.get("match_all", False)

    logger.info(f"Splitting data based on the property: {criteria}")
    train_images = []
    val_images = []
    train_annotations = []
    val_annotations = []

    for image in coco_data["images"]:
        if match_all:
            match = all(
                key in image and any(str(value) in str(image[key]) for value in values)
                for key, values in criteria.items()
            )
        else:
            match = any(
                key in image and any(str(value) in str(image[key]) for value in values)
                for key, values in criteria.items()
            )

        if match:
            val_images.append(image)
            val_annotations.extend(
                [
                    ann
                    for ann in coco_data["annotations"]
                    if ann["image_id"] == image["id"]
                ]
            )
        else:
            train_images.append(image)
            train_annotations.extend(
                [
                    ann
                    for ann in coco_data["annotations"]
                    if ann["image_id"] == image["id"]
                ]
            )

    train_data = {
        "info": coco_data.get("info", {}),
        "licenses": coco_data.get("licenses", []),
        "images": train_images,
        "annotations": train_annotations,
        "categories": coco_data["categories"],
    }
    val_data = {
        "info": coco_data.get("info", {}),
        "licenses": coco_data.get("licenses", []),
        "images": val_images,
        "annotations": val_annotations,
        "categories": coco_data["categories"],
    }

    for data_type, data in [("train", train_data), ("val", val_data)]:
        file_path = f"{output_filename}_{data_type}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved split into {file_path}")
