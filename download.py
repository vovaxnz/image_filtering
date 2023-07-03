import os
import shutil
import argparse

from api_requests import get_source_video_path
from path_manager import PathManager
from ssh_utils import ssh_download
from utils import move_nested_files, unzip_files_in_folder


def download(project_id):

    pm = PathManager(project_id)
    
    # Get remote video path
    remote_source_video = get_source_video_path(project_id)

    print('remote_source_video', remote_source_video)
    # Download video
    ssh_download(
        local_path=pm.video_path, 
        remote_path=remote_source_video
    )
    
    if not os.path.isfile(pm.video_path):
        print('It looks like video has not been downloaded. Ask to create a video')
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int)
    args = parser.parse_args()

    download(project_id=args.n)