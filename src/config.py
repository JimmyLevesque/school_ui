from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Settings(BaseSettings):
    API_URL: str

    class Config:
        env_file = ".env"


settings = Settings()