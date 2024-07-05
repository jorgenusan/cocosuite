# COCOSuite

COCOSuite is a comprehensive collection of tools designed to facilitate the management and manipulation of datasets in COCO format.

## Tools

| Tool | Description |
| ---- | ----------- |
| [coco_merge](./cocosuite/scripts/manipulation/coco_merge.py) | Merge two COCO datasets into a single one |
| [merge_multiple](./cocosuite/scripts/manipulation/merge_multiple_coco_files.py) | Allows merging of multiple COCO files into a single dataset |
| [coco_split](./cocosuite/scripts/manipulation/coco_split.py) | It consists of two functions, **`random_split`** performs a random division of the dataset into training and validation subsets, configurable in terms of data proportion, and **`property_split`** divides a COCO dataset into training and validation sets according to specific image properties |
| [coco_filter](./cocosuite/scripts/manipulation/coco_filter.py) | Filters a COCO dataset based on certain criteria |
| [visualization](./cocosuite/scripts/visualization/visualization.py) | A series of visualization charts for analyzing and understanding data distributions, image sizes, annotation counts, and bounding box sizes within a dataset. |

## Installation

- Pip

  Install COCOSuite directly from PyPI:

  ```bash
  pip install cocosuite
  ```

- Source

  Clone the repository and install the dependencies:

  ```bash
  git clone https://github.com/jorgenusan/cocosuite.git
  cd cocosuite
  pip install -r requirements.txt
  ```

## Usage

> [!IMPORTANT]
> In all scripts, if no path is specified in the <output_filename> argument and only a name is specified. The resulting file will be created in the input annotations file path

### Basic example

```bash
python3 /cocosuite/scripts/manipulation/coco_merge.py <annotations_file_1> <annotations_file_2> <output_filename>
```

### config_split

Applies to **property_split** and **coco_filter**

```bash
python3 /cocosuite/scripts/manipulation/property_split.py <annotations_file> <config_split>
```

For these scripts you have to pass a configuration file with the criteria for separating the data in the case of **property_split** and the criteria for filtering in the case of **coco_filter**.

Here is an example for each of these cases:

1. property_split

   ```json
    "criteria": {
      "file_name": ["image1", "image2"],
      "height": [480]
    },
    "match_all": true
   ```

2. coco_filter

    ```json
    "filter": {
      "file_name": ["image1", "image2"],
      "height": [480]
    },
    "match_all": true
   ```

> [!NOTE]
> the **match_all** property, when set to `true` means that both properties have to match in order to filter or split a new file.<br>
> If set to `false`, it filters or splits for each property.
