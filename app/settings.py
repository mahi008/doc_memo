from pydantic import BaseModel
import os


class APPSettings(BaseModel):
    MONGO_DB_HOST: str = os.getenv("DB_HOST")
    MONGO_DB_NAME: str = os.getenv("DB_NAME")
    MONGO_DB_USER: str = os.getenv("DB_USER")
    MONGO_DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    MONGO_DB_PORT: str = os.getenv("DB_PORT")
