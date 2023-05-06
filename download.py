import os
import shutil
import argparse

from api_requests import get_source_archive_dir
from path_manager import PathManager
from ssh_utils import ssh_download
from utils import move_nested_files, unzip_files_in_folder


def download(project_id):

    pm = PathManager(project_id)
    
    # Get remote archive path
    remote_source_dir = get_source_archive_dir(project_id)

    # Download archive
    ssh_download(
        local_dir=pm.download_dir, 
        remote_dir=remote_source_dir
    )
    
    if len(os.listdir(pm.download_dir)) == 0:
        print('It looks like no archive has been downloaded. Ask to create an archive')
        return

    # Unzip archive
    unzip_files_in_folder(
        source_dir=pm.download_dir, 
        result_dir=pm.unzip_dir
    )

    # Remove unnecessary archive
    shutil.rmtree(pm.download_dir)

    # Move images to source images dir
    move_nested_files(
        source_dir=pm.unzip_dir, 
        dest_dir=pm.source_images_dir
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int)
    args = parser.parse_args()

    download(project_id=args.n)