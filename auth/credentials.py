import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

CREDENTIALS = {
    os.getenv("ADMIN_USER"): os.getenv("ADMIN_PASS")
}