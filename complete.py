import os
import shutil
import argparse

from api_requests import complete_project, get_selected_images_dir
from path_manager import PathManager
from ssh_utils import ssh_upload
from utils import open_json


def complete(project_id: int):
    
    pm = PathManager(project_id)

    # Check that selected dir is not empty
    if len(os.listdir(pm.selected_images_dir)) == 0:
        input(f"You have not selected any images in the {project_id} project. Press Enter if this is true. Or press CTRL+C if you haven't started filtering this project yet, and start filtering this project via command: python3 filtering.py -n <project_id>.")

    # Get selected images remote dir
    remote_selected_dir = get_selected_images_dir(project_id=project_id)
    
    # Upload images to the remote directory
    ssh_upload(
        local_dir=pm.selected_images_dir, 
        remote_dir=remote_selected_dir
    )

    # Remove source images
    shutil.rmtree(pm.source_images_dir)

    # Mark project as completed
    complete_project(
        project_id=project_id, 
        duration_hours=round(open_json(pm.project_json_path)["duration"] / 3600, 2)
    )

    print(f'✅ Filtering Project #{project_id} completed!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int)
    args = parser.parse_args()

    complete(project_id=args.n)
