import os
from config import address

def ssh_upload(local_dir: str, remote_dir: str):
    os.system(f"scp -r {local_dir} {address}:{remote_dir}")

def ssh_download(local_dir: str, remote_dir: str):
    os.system(f"scp -r {address}:{remote_dir} {local_dir}")
