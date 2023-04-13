import os
from typing import Dict
import cv2
import shutil
import time
import json
import numpy as np
from datetime import datetime
import argparse


def save_json(
    value,
    file_path,
):
    with open(file_path, "w") as filename:
        json.dump(value, filename)


def open_json(detections_file) -> Dict:
    with open(detections_file) as file:
        value = json.load(file)
    return value

def main(
    source_img_dir: str,
    selected_img_dir: str,
    window_height: int,
    window_width: int,
    short_delay_ms: int,
    normal_delay_ms: int,
    long_delay_ms: int,
    max_action_time_sec: int = 5,
):
    os.makedirs(selected_img_dir, exist_ok=True)

    dir_create_time = os.stat(source_img_dir).st_mtime
    dir_creation_datetime_str = datetime.fromtimestamp(int(dir_create_time)).strftime("%Y-%m-%d_%H-%M-%S")
    
    json_info_name = source_img_dir.replace(os.sep, "-")[1:] + "_" + dir_creation_datetime_str + ".json"
    json_info_name = json_info_name[-100:]    


    info_json_path = os.path.join(os.path.dirname(__file__), json_info_name)
    if os.path.isfile(info_json_path):
        img_id = open_json(info_json_path)["img_id"]
        duration = open_json(info_json_path)["duration"]
    else:
        save_json({"img_id": 0, "duration": 0}, info_json_path)
        img_id = 0
        duration = 0

    img_names = sorted(os.listdir(source_img_dir))

    total_number_of_images = len(img_names)
    start_time = time.time()
    update_image = True
    delay = short_delay_ms
    img_counter = img_id
    last_img_id = img_id

    while True:

        if update_image:
            source_img_path = os.path.join(source_img_dir, img_names[img_id])

            img = cv2.imread(source_img_path)
            if img is None:
                img = np.zeros((window_width, window_height, 3), np.uint8)
                cv2.putText(img, f"Image broken: {img_names[img_id]}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(img, "Move on and continue filtering", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                
            img = cv2.resize(img, (window_height, window_width))
            cv2.imshow('output', img)

            curr_time = time.time()
            step_duration = min(curr_time - start_time, max_action_time_sec)
            start_time = curr_time
            duration += step_duration
            save_json({"img_id": img_id, "duration": duration}, info_json_path)
            print(f'Image ID: {img_id}, Processed {round(img_id / total_number_of_images * 100, 2)}% of images, Your speed: {int(img_counter / duration * 3600)} images/hour, filtering_duration: {round(duration / 3600, 3)} hours')

        k = cv2.waitKey(0)
        time.sleep(delay / 1000)

        # backward
        if k == ord('a'):
            img_id -= 1
            img_id = max(0, img_id)
            update_image = True
            delay=normal_delay_ms

        # forward
        if k == ord('w'):
            img_id += 1
            img_id = min(len(img_names) - 1, img_id)
            update_image = True
            delay=short_delay_ms
        if k == ord('s'):
            img_id += 1
            img_id = min(len(img_names) - 1, img_id)
            update_image = True
            delay=normal_delay_ms
        if k == ord('x'):
            img_id += 1
            img_id = min(len(img_names) - 1, img_id)
            update_image = True
            delay=long_delay_ms

        if img_id > last_img_id:
            img_counter += 1
            last_img_id = img_id

        if img_id == total_number_of_images - 1:
            print('You processed all images! 🎉')
            break


        if k == ord('c'):
            print('copied', img_names[img_id])
            shutil.copy(
                os.path.join(source_img_dir, img_names[img_id]),
                os.path.join(selected_img_dir, img_names[img_id])
            )
            
            img_id += 1
            img_id = min(len(img_names) - 1, img_id)
            update_image = True

        if k == ord('p'):
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str)
    parser.add_argument("--selected", type=str)
    parser.add_argument("--window_height", type=int, default=1280)
    parser.add_argument("--window_width", type=int, default=720)
    parser.add_argument("--short_delay_ms", type=int, default=5)
    parser.add_argument("--normal_delay_ms", type=int, default=40)
    parser.add_argument("--long_delay_ms", type=int, default=100)
    args = parser.parse_args()
    
    main(
        source_img_dir=args.source,
        selected_img_dir=args.selected,

        window_height=args.window_height,
        window_width=args.window_width,
        
        short_delay_ms=args.short_delay_ms,
        normal_delay_ms=args.normal_delay_ms,
        long_delay_ms=args.long_delay_ms,
    )
            
