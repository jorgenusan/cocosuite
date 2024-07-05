import json

from common import plot_bar_chart, plot_scatter_chart


def plot_cat_distribution(annotations_file: str) -> None:
    """Plot the distribution of categories in the input json file.

    Args:
        annotations_file (str): JSON file containing COCO formatted data.
    """
    with open(annotations_file, "r") as f:
        coco_data = json.load(f)

    categories = {cat["name"]: 0 for cat in coco_data["categories"]}
    for ann in coco_data["annotations"]:
        categories[coco_data["categories"][ann["category_id"] - 1]["name"]] += 1

    plot_bar_chart(categories, "Categories", "Count", "Category Distribution")


def plot_img_size_distribution(annotation_file: str) -> None:
    """Plot the distribution of image sizes in the input json file.

    Args:
        annotation_file (str): JSON file containing COCO formatted data.
    """
    with open(annotation_file, "r") as f:
        coco_data = json.load(f)

    image_sizes: dict = {}
    for image in coco_data["images"]:
        size = (image["width"], image["height"])
        if size in image_sizes:
            image_sizes[size] += 1
        else:
            image_sizes[size] = 1

    img_data = {f"{size[0]}x{size[1]}": count for size, count in image_sizes.items()}

    plot_bar_chart(img_data, "Image Size", "Count", "Image Size Distribution")


def plot_annotations_per_img(annotation_file: str) -> None:
    """Plot the number of annotations per image in the input json file.

    Args:
        annotation_file (str): JSON file containing COCO formatted data.
    """
    with open(annotation_file, "r") as f:
        coco_data = json.load(f)

    annotations_per_img = {img["file_name"]: 0 for img in coco_data["images"]}
    for ann in coco_data["annotations"]:
        annotations_per_img[coco_data["images"][ann["image_id"] - 1]["file_name"]] += 1

    plot_bar_chart(
        annotations_per_img,
        "Images",
        "Number of Annotations",
        "Number of Annotations per Image",
    )


def plot_img_size_distribution_by_category(annotation_file: str) -> None:
    """Plot the distribution of image sizes by category in the input json file.

    Args:
        annotation_file (str): JSON file containing COCO formatted data.
    """
    with open(annotation_file, "r") as f:
        coco_data = json.load(f)

    category_names = {cat["id"]: cat["name"] for cat in coco_data["categories"]}

    widths = []
    heights = []
    categories = []

    for ann in coco_data["annotations"]:
        image = next(
            (img for img in coco_data["images"] if img["id"] == ann["image_id"]), None
        )
        if image:
            widths.append(image["width"])
            heights.append(image["height"])
            categories.append(category_names[ann["category_id"]])

    plot_scatter_chart(
        widths,
        heights,
        categories,
        "Width",
        "Height",
        "Image Size Distribution by Category",
        "Categories",
    )


def plot_bbox_size_distribution_by_category(annotation_file: str) -> None:
    """Plot the distribution of bounding box sizes by category in the input json file.

    Args:
        annotation_file (str): JSON file containing COCO formatted data.
    """
    with open(annotation_file, "r") as f:
        coco_data = json.load(f)

    category_names = {cat["id"]: cat["name"] for cat in coco_data["categories"]}

    bbox_widths = []
    bbox_heights = []
    categories = []

    for ann in coco_data["annotations"]:
        bbox = ann["bbox"]
        bbox_widths.append(bbox[2])
        bbox_heights.append(bbox[3])
        categories.append(category_names[ann["category_id"]])

    plot_scatter_chart(
        bbox_widths,
        bbox_heights,
        categories,
        "Width",
        "Height",
        "Bounding Box Size Distribution",
        "Categories",
    )
