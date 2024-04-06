import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
address = os.getenv("ADDRESS")
data_dir = os.getenv("DATA_DIR")

assert token is not None
assert address is not None
assert data_dir is not None


short_delay_ms=5
normal_delay_ms=40
long_delay_ms=100
