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
    source_video_path: str,
    selected_img_dir: str,
    info_json_path: str,
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

    cv2.namedWindow("output", cv2.WINDOW_NORMAL)  

    cap = cv2.VideoCapture(source_video_path)

    cap.set(cv2.CAP_PROP_POS_FRAMES, img_id)

    # Check if the video file was successfully opened
    if not cap.isOpened():
        print("Error opening video file")

    # Get the total number of frames in the video
    total_number_of_images = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    start_time = time.time()
    update_image = True
    delay = short_delay_ms
    img_counter = img_id
    last_img_id = img_id
    move_backward = False 

    while True:

        if update_image:

            if move_backward:
                cap.set(cv2.CAP_PROP_POS_FRAMES, img_id)
                move_backward = False

            ret, orig_img = cap.read()
       
            img = orig_img

            # tuning progress bar
            text = f'ImgID: {img_id}, Prcsd {round(img_id / total_number_of_images * 100, 2)}%'
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

            update_image = False

        k = cv2.waitKey(0)
        time.sleep(delay / 1000)

        # backward
        if k == ord('a'):
            img_id -= 1
            img_id = max(0, img_id)
            update_image = True
            delay=normal_delay_ms
            move_backward = True

        # forward
        if k == ord('w'):
            img_id += 1
            img_id = min(total_number_of_images - 1, img_id)
            update_image = True
            delay=short_delay_ms
        if k == ord('s'):
            img_id += 1
            img_id = min(total_number_of_images - 1, img_id)
            update_image = True
            delay=normal_delay_ms
        if k == ord('x'):
            img_id += 1
            img_id = min(total_number_of_images - 1, img_id)
            update_image = True
            delay=long_delay_ms

        if img_id > last_img_id:
            img_counter += 1
            last_img_id = img_id



        if k == ord('c'):
            print('copied', img_id)
            cv2.imwrite(os.path.join(selected_img_dir, f"{str(img_id).zfill(6)}.jpg"), orig_img)
            img_id += 1
            img_id = min(total_number_of_images - 1, img_id)
            update_image = True

        if k == ord('p'):
            break

        if img_id == total_number_of_images - 1:
            print('You processed all images! 🎉')
            break
    cap.release()
    cv2.destroyAllWindows()


def start_filtering(project_id: int):

    pm = PathManager(project_id)

    assert os.path.isfile(pm.video_path), f"No video found. Download filtering project via command: python3 download.py -n {project_id}"

    filtering(
        source_video_path=pm.video_path,
        selected_img_dir=pm.selected_images_dir,

        info_json_path=pm.project_json_path,

        
        short_delay_ms=config.short_delay_ms,
        normal_delay_ms=config.normal_delay_ms,
        long_delay_ms=config.long_delay_ms,
    )
       


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int)
    args = parser.parse_args()

    start_filtering(project_id=args.n)
