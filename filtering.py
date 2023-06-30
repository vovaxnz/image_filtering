import os
from typing import Dict
import cv2
import shutil
import time
import numpy as np
import argparse
from path_manager import PathManager

from utils import open_json, save_json

import config


def filtering(
    source_img_dir: str,
    selected_img_dir: str,
    info_json_path: str,
    window_width: int,
    window_height: int,
    short_delay_ms: int,
    normal_delay_ms: int,
    long_delay_ms: int,
    max_action_time_sec: int = 5,
):
    os.makedirs(selected_img_dir, exist_ok=True)

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
                img = np.zeros((window_height, window_width, 3), np.uint8)
                cv2.putText(img, f"Image broken: {img_names[img_id]}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(img, "Move on and continue filtering", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                

            img = cv2.resize(img, (window_width, window_height))

            # tuning progress bar
            text = f'ImgID: {img_id}, Prcsd {round(img_id / len(img_names) * 100, 2)}%'
            font = cv2.FONT_HERSHEY_PLAIN
            org = (50, 50)
            color = (0, 255, 0)
            thickness = 2
            cv2.putText(img, text, org, font, 1, color, thickness)


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


def start_filtering(project_id: int):

    pm = PathManager(project_id)

    assert len(os.listdir(pm.source_images_dir)) > 0, f"No images found. Download filtering project first via command: python3 download.py -n {project_id}"

    filtering(
        source_img_dir=pm.source_images_dir,
        selected_img_dir=pm.selected_images_dir,

        info_json_path=pm.project_json_path,

        window_width=config.window_width,
        window_height=config.window_height, 
        
        short_delay_ms=config.short_delay_ms,
        normal_delay_ms=config.normal_delay_ms,
        long_delay_ms=config.long_delay_ms,
    )
       


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int)
    args = parser.parse_args()

    start_filtering(project_id=args.n)
