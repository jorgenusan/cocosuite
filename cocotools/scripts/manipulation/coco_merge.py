import json
from pathlib import Path
from typing import Any, Dict

import fire
from loguru import logger


def coco_merge(
    annotations_file_1: str,
    annotations_file_2: str,
    output_filename: str = "merged_annotations.json",
) -> str:
    """Merge two COCO formatted json files into a single file.

    Args:
        annotations_file_1 (str): File path to the first COCO formatted json file.
        annotations_file_2 (str): File path to the second COCO formatted json file.
        output_filename (str, optional): Name of the output json file. Defaults to "merged_annotations.json".

    Returns:
        str: Path to the output json file.
    """
    with open(annotations_file_1, "r") as f:
        data_1 = json.load(f)
    with open(annotations_file_2, "r") as f:
        data_2 = json.load(f)

    output: Dict[str, Any] = {
        k: data_1[k] for k in data_1 if k not in ("images", "annotations")
    }

    output["images"], output["annotations"] = [], []

    for i, data in enumerate([data_1, data_2]):
        logger.info(
            "Input {}: {} images, {} annotations".format(
                i + 1, len(data["images"]), len(data["annotations"])
            )
        )

        cat_id_map = {}
        for new_cat in data["categories"]:
            new_id = None
            for output_cat in output["categories"]:
                if new_cat["name"] == output_cat["name"]:
                    new_id = output_cat["id"]
                    break

            if new_id is not None:
                cat_id_map[new_cat["id"]] = new_id
            else:
                new_cat_id = max(c["id"] for c in output["categories"]) + 1
                cat_id_map[new_cat["id"]] = new_cat_id
                new_cat["id"] = new_cat_id
                output["categories"].append(new_cat)

        img_id_map = {}
        for image in data["images"]:
            n_imgs = len(output["images"])
            img_id_map[image["id"]] = n_imgs
            image["id"] = n_imgs

            output["images"].append(image)

        for annotation in data["annotations"]:
            n_anns = len(output["annotations"])
            annotation["id"] = n_anns
            annotation["image_id"] = img_id_map[annotation["image_id"]]
            annotation["category_id"] = cat_id_map[annotation["category_id"]]

            output["annotations"].append(annotation)

    logger.info(
        "Result: {} images, {} annotations".format(
            len(output["images"]), len(output["annotations"])
        )
    )

    if len(output_filename.rsplit("/", 1)) < 2:
        file_path = Path(annotations_file_1).parent
        output_filename = str(Path(file_path, output_filename))

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return str(output_filename)


if __name__ == "__main__":
    fire.Fire(coco_merge)
