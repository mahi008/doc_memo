from pymongo import MongoClient
from pymongo.errors import PyMongoError

from settings import APPSettings

app_settings = APPSettings()


def get_db():
    db_uri = (
        f"mongodb://{app_settings.MONGO_DB_USER}:{app_settings.MONGO_DB_PASSWORD}"
        f"@{app_settings.MONGO_DB_HOST}:{app_settings.MONGO_DB_PORT}/?authSource=admin"
    )
    try:
        db_client = MongoClient(db_uri)
        database = db_client[app_settings.MONGO_DB_NAME]
        return database
    except PyMongoError as e:
        raise e
