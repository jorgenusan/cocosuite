# COCO Toolkit

## Introduction

COCO Toolkit is a collection of tools designed to facilitate the handling and processing of datasets in COCO format.

## Tools

| Tool | Description |
| ---- | ----------- |
| [coco_merge](./cocotoolkit/scripts/manipulation/coco_merge.py) | Merge two COCO datasets into a single one |
| [merge_multiple](./cocotoolkit/scripts/manipulation/merge_multiple_coco_files.py) | Allows merging of multiple COCO files into a single dataset |
| [random_split](./cocotoolkit/scripts/manipulation/random_split.py) | Performs a random division of the dataset into training and validation subsets, configurable in terms of data proportion. |
| [property_split](./cocotoolkit/scripts/manipulation/property_split.py) | Divides a COCO dataset into training and validation sets according to specific image properties |
| [coco_filter](./cocotoolkit/scripts/manipulation/coco_filter.py) | Filters a COCO dataset based on certain criteria |

## Installation

```bash
git clone https://github.com/jorgenusan/cocotoolkit.git
cd cocotools
pip3 install -r requirements.txt
```

## Usage

> [!IMPORTANT]
> In all scripts, if no path is specified in the <output_filename> argument and only a name is specified. The resulting file will be created in the input annotations file path

### Basic example

```bash
python3 /cocotoolkit/scripts/manipulation/coco_merge.py <annotations_file_1> <annotations_file_2> <output_filename>
```

### config_split

Applies to **property_split** and **coco_filter**

```bash
python3 /cocotoolkit/scripts/manipulation/property_split.py <annotations_file> <config_split>
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
      "file_name": ["imagen1", "imagen2"],
      "height": [480]
    },
    "match_all": true
   ```

> [!NOTE]
> the **match_all** property, when set to `true` means that both properties have to match in order to filter or split a new file.<br>
> If set to `false`, it filters or splits for each property.
