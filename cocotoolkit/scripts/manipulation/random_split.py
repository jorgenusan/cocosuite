import json
import random
from pathlib import Path

import fire
import numpy as np
from loguru import logger


def random_split(
    annotations_file: str,
    output_filename: str = "random_split.json",
    train_percentage: float = 0.8,
    seed: int = 47,
) -> None:
    """Split the input json file randomly into train and val.

    Args:
        annotations_file (str): JSON file containing COCO formatted data.
        output_filename (Optional[str], optional): Name of the output json file. Defaults to None.
        output_path (Optional[str], optional): Path to save the output file. Defaults to None.
        train_percentage (Optional[float], optional): Percentage of data to be used for training. Defaults to 0.8.
        seed (Optional[int], optional): Seed for random number generation. Defaults to 47.
    """
    with open(annotations_file, "r") as f:
        data = json.load(f)

    random.seed(seed)
    np.random.seed(seed)

    logger.info(
        f"Splitting data into train and val with {train_percentage} train percentage"
    )
    data_size = len(data["images"])
    indices = np.random.permutation(data_size)
    train_size = int(data_size * train_percentage)
    train_indices = indices[:train_size]
    val_indices = indices[train_size:]

    train_data = {
        "info": data.get("info", {}),
        "licenses": data.get("licenses", []),
        "images": [],
        "annotations": [],
        "categories": data["categories"],
    }
    val_data = {
        "info": data.get("info", {}),
        "licenses": data.get("licenses", []),
        "images": [],
        "annotations": [],
        "categories": data["categories"],
    }

    train_data["images"] = [data["images"][i] for i in train_indices]
    val_data["images"] = [data["images"][i] for i in val_indices]

    for ann in data["annotations"]:
        if ann["image_id"] in train_indices:
            train_data["annotations"].append(ann)
        else:
            val_data["annotations"].append(ann)

    file_name = Path(output_filename).stem
    if len(output_filename.rsplit("/", 1)) >= 2:
        file_path = Path(output_filename).parent
    else:
        file_path = Path(annotations_file).parent

    for data_type, data in [("train", train_data), ("val", val_data)]:
        type_file_name = f"{file_name}_{data_type}.json"
        output_file = Path(file_path, type_file_name)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved split into {type_file_name}")


if __name__ == "__main__":
    fire.Fire(random_split)
