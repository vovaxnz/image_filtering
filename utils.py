import json
import yaml
import os
import shutil
from typing import List


def save_json(
    value,
    file_path,
):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as filename:
        json.dump(value, filename, indent=4)


def open_json(detections_file) -> dict:
    with open(detections_file) as file:
        value = json.load(file)
    return value


def unzip_files_in_folder(source_dir, result_dir):
    curr_dir = os.getcwd()
    os.chdir(source_dir)
    os.makedirs(result_dir, exist_ok=True)
    file_paths = get_file_paths(source_dir)
    for file_path in file_paths:
        os.system(f"unzip {file_path} -d {result_dir}")
    os.chdir(curr_dir)


def get_file_paths(source_dir_path: str) -> List[str]:
    paths = list()
    for dirpath, dirnames, filenames in os.walk(source_dir_path):
        for filename in filenames:
            paths.append(os.path.join(dirpath, filename))
    return paths


def move_files(file_paths: List[str], dest_dir: str):
    for file_path in file_paths:
        shutil.move(file_path, dest_dir)


def move_nested_files(source_dir, dest_dir):
    file_paths = get_file_paths(source_dir_path=source_dir)
    move_files(file_paths=file_paths, dest_dir=dest_dir)