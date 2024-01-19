import shutil
import os
import json
from constants import *


def init_annotations_dirs(annotations_dirpath):
    success = True
    with open(FIELD_INCLUSION, "r", encoding="utf-8") as file:
        fields_dict = json.load(file)
        for element_id, include_field in fields_dict.items():
            dir_path = os.path.join(annotations_dirpath, element_id)
            try:
                os.makedirs(dir_path, exist_ok=True)
            except OSError as e:
                success = False
                print(f"Error: {e}")
    if success:
        print(f"Directories for annotations created successfully.")


def init_dir(dir_path):
    try:
        os.makedirs(dir_path, exist_ok=True)
        # print(f"Directory '{dir_path}' created successfully.")
    except OSError as e:
        print(f"Error: {e}")


def remove_dir(dir_path):
    try:
        shutil.rmtree(dir_path)
        # print(f"Directory '{dir_path}' removed successfully.")
    except OSError as e:
        print(f"Error: {e}")
