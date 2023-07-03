import os
from config import address

def ssh_upload(local_dir: str, remote_dir: str):
    os.system(f"scp -r {local_dir} {address}:{remote_dir}")

def ssh_download(local_path: str, remote_path: str):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    os.system(f"scp -r {address}:{remote_path} {local_path}")
