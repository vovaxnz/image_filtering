import os
import shutil
import argparse

from api_requests import complete_project, get_number_of_uploaded_images, get_selected_images_dir
from path_manager import PathManager
from ssh_utils import ssh_upload
from utils import open_json


def complete(project_id: int):
    
    pm = PathManager(project_id)

    # Get selected images remote dir
    remote_selected_dir = get_selected_images_dir(project_id=project_id)
    
    # Upload images to the remote directory
    ssh_upload(
        local_dir=pm.selected_images_dir, 
        remote_dir=remote_selected_dir
    )

    # API request to patform to get number of uploaded images
    number_of_uploaded_images = get_number_of_uploaded_images(project_id=project_id)

    # If 0 images uploaded - ask for confirmation
    if number_of_uploaded_images == 0:
        input(f"You are going to complete project {project_id} without a single selected image. The entire filtering project will be deleted. Press Enter to confirm. Or press CTRL+C if you are not going to complete project {project_id}.")

    # Remove source video
    if os.path.isfile(pm.video_path):
        os.remove(pm.video_path)

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
