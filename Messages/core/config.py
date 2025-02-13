from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
import os

from typing import ClassVar


class Settings(BaseSettings):

    DATABASE_URL: str = 'postgresql://postgres:ghazaldb1@localhost:5432/messages'




def get_settings() -> Settings:
    return Settings()