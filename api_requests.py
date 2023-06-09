import requests
from config import token


def get_source_video_path(project_id: int) -> str:
    url = f'https://eg-ml.com/api/filtering_project/source_video/{project_id}/'

    data = {'user_token': token}
    response = requests.post(url, json=data)

    if response.status_code != 200:
        raise RuntimeError(response.json()["message"])
    
    return response.json()["value"]


def get_selected_images_dir(project_id: int) -> str:
    url = f'https://eg-ml.com/api/filtering_project/selected_dir/{project_id}/'

    data = {'user_token': token}
    response = requests.post(url, json=data)

    if response.status_code != 200:
        raise RuntimeError(response.json()["message"])
    
    return response.json()["value"]


def complete_project(project_id: int, duration_hours: float):
    url = f'https://eg-ml.com/api/filtering_project/complete/{project_id}/'

    data = {'user_token': token, 'duration_hours': duration_hours}
    response = requests.post(url, json=data)

    if response.status_code != 200:
        raise RuntimeError(response.json()["message"])
    

def get_number_of_uploaded_images(project_id: int) -> int:
    url = f'https://eg-ml.com/api/filtering_project/number_of_selected/{project_id}/'

    data = {'user_token': token}
    response = requests.post(url, json=data)

    if response.status_code != 200:
        raise RuntimeError(response.json()["message"])
    
    return response.json()["value"]