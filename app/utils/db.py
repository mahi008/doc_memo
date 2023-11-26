from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError

from settings import APPSettings

app_settings = APPSettings()


def get_db() -> Database:
    """
    Get a connection to the MongoDB database.
    Returns:
        Database: The MongoDB client object.
    Raises:
        PyMongoError: If there is an error connecting to the database.
    """
    try:
        db_client = MongoClient(
            f"mongodb://{app_settings.MONGO_DB_USER}:{app_settings.MONGO_DB_PASSWORD}"
            f"@{app_settings.MONGO_DB_HOST}:{app_settings.MONGO_DB_PORT}/?authSource=admin"
        )
        database = db_client[app_settings.MONGO_DB_NAME]
        return database
    except PyMongoError as e:
        raise
