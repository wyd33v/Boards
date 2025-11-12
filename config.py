
import os

from dotenv import load_dotenv

load_dotenv(".env")

class Config:
    DB_PATH = f'data/{os.getenv("DB_NAME")}'
    CACHE_PORT = os.getenv('CACHE_PORT')
