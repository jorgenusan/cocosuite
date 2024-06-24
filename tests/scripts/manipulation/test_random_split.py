import pytest

from cocotools.scripts.manipulation.random_split import random_split
from pathlib import Path


@pytest.mark.parametrize("input_json", [
    "examples/coco_examples_1.json",
    "examples/coco_examples_2.json",
])
def test_random_split(input_json):
    output_file = "examples/random_split_output"

    random_split(input_json, output_file, train_percentage=0.8, seed=47)
    
    assert Path(f"{output_file}_train.json").exists()
    assert Path(f"{output_file}_val.json").exists()
    