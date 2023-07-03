import os

from config import data_dir


class PathManager():

    def __init__(self, project_id: int):
        self.project_name = str(project_id).zfill(5)

        os.makedirs(os.path.dirname(self.video_path), exist_ok=True)
        os.makedirs(self.selected_images_dir, exist_ok=True)
        os.makedirs(self.meta_dir, exist_ok=True)

    @property
    def data_dir(self):
        return os.path.join(data_dir, "data")
    
    @property
    def meta_dir(self):
        return os.path.join(data_dir, "meta")
    
    @property
    def temp_dir(self):
        return os.path.join(data_dir, "temp")
    
    @property
    def video_path(self):
        return os.path.join(self.data_dir, self.project_name, "video.mp4")
    
    @property
    def selected_images_dir(self):
        return os.path.join(self.data_dir, self.project_name, "selected")
    
    @property
    def project_json_path(self):
        return os.path.join(self.meta_dir, f"{self.project_name}.json")