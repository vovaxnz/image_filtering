import os

from config import data_dir


class PathManager():

    def __init__(self, project_id: int):
        self.project_name = str(project_id).zfill(5)

        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.unzip_dir, exist_ok=True)
        os.makedirs(self.source_images_dir, exist_ok=True)
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
    def download_dir(self):
        return os.path.join(self.temp_dir, self.project_name, "download")
    
    @property
    def unzip_dir(self):
        return os.path.join(self.temp_dir, self.project_name, "unzipped")
    
    @property
    def source_images_dir(self):
        return os.path.join(self.data_dir, self.project_name, "source")
    
    @property
    def selected_images_dir(self):
        return os.path.join(self.data_dir, self.project_name, "selected")
    
    @property
    def project_json_path(self):
        return os.path.join(self.meta_dir, f"{self.project_name}.json")