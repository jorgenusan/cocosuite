import json
import random
import numpy as np
from loguru import logger

def random_split(input_json: str, output_file: str, train_percentage: float = 0.8, seed: int = 47):
    """Split the input json file into train and val json files based on the train_percentage

    Args:
        input_json (str): JSON file containing COCO formatted data.
        output_file (str): Prefix of the output json files.
        train_percentage (float, optional): Percentage of data to be used for training. Defaults to 0.8.
        seed (int, optional): Seed for reproducibility. Defaults to 47.
    """
    with open (input_json, 'r') as f:
        data = json.load(f)
    
    random.seed(seed)
    np.random.seed(seed)

    logger.info(f"Splitting data into train and val with {train_percentage} train percentage")
    data_size = len(data['images'])
    indices = np.random.permutation(data_size)
    train_size = int(data_size * train_percentage)
    train_indices = indices[:train_size]
    val_indices = indices[train_size:]

    train_data = {
        'info': data.get('info', {}),
        'licenses': data.get('licenses', []),
        'images': [], 
        'annotations': [], 
        'categories': data['categories']
    }
    val_data = {
        'info': data.get('info', {}),
        'licenses': data.get('licenses', []),
        'images': [], 
        'annotations': [], 
        'categories': data['categories']
    }
    
    train_data['images'] = [data['images'][i] for i in train_indices]
    val_data['images'] = [data['images'][i] for i in val_indices]

    for ann in data['annotations']:
        if ann['image_id'] in train_indices:
            train_data['annotations'].append(ann)
        else:
            val_data['annotations'].append(ann)

    for data_type, data in [('train', train_data), ('val', val_data)]:
        file_path = f"{output_file}_{data_type}.json"
        with open(file_path, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved split into {file_path}") 
