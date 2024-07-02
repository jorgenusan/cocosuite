import pytest
import json
import tempfile
from pathlib import Path
from cocosuite.scripts.manipulation.coco_merge import coco_merge


def load_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def create_empty_coco_file():
    empty_coco_data = {
        "images": [],
        "annotations": [],
        "categories": [],
        "info": {},
        "licenses": []
    }
    return empty_coco_data


def test_coco_merge_with_example_files(project_root_path):
    file1_path = project_root_path / "examples/coco_example_1.json"
    file2_path = project_root_path / "examples/coco_example_2.json"
    
    data1 = load_json_file(file1_path)
    data2 = load_json_file(file2_path)
    
    expected_num_images = len(data1.get("images", [])) + len(data2.get("images", []))
    expected_num_annotations = len(data1.get("annotations", [])) + len(data2.get("annotations", []))
    expected_num_categories = len({cat["name"] for cat in data1.get("categories", []) + data2.get("categories", [])})
    
    with tempfile.NamedTemporaryFile(delete=True) as tmpfile:
        result_file = coco_merge(file1_path, file2_path, tmpfile.name)
        
        assert Path(result_file).exists()
        
        with open(result_file, "r") as f:
            merged_data = json.load(f)
        
        assert len(merged_data["images"]) == expected_num_images
        assert len(merged_data["annotations"]) == expected_num_annotations
        assert len(merged_data["categories"]) == expected_num_categories


def test_coco_merge_with_empty_file(project_root_path):
    file1_path = project_root_path / "examples/coco_example_1.json"
    
    data1 = load_json_file(file1_path)
    
    expected_num_images = len(data1.get("images", []))
    expected_num_annotations = len(data1.get("annotations", []))
    expected_num_categories = len(data1.get("categories", []))
    
    with tempfile.NamedTemporaryFile(mode='w+', delete=True, suffix='.json') as empty_file:
        empty_coco_data = create_empty_coco_file()
        json.dump(empty_coco_data, empty_file)
        empty_file.flush()
        
        with tempfile.NamedTemporaryFile(delete=True) as tmpfile:
            result_file = coco_merge(str(file1_path), empty_file.name, tmpfile.name)
            
            assert Path(result_file).exists()
            
            with open(result_file, "r") as f:
                merged_data = json.load(f)
            
            assert len(merged_data["images"]) == expected_num_images
            assert len(merged_data["annotations"]) == expected_num_annotations
            assert len(merged_data["categories"]) == expected_num_categories
