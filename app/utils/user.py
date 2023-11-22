from typing import Union

from gridfs import GridOutCursor
from models import User, Patient, CareGiver, Professional
from pymongo.errors import PyMongoError
from utils.password_helper import PasswordHelper
import logging

logger = logging.getLogger(__name__)


class UserManager:
    collection = None
    db_conn = None

    def __init__(self, db_conn, collection_name):
        self.db_conn = db_conn
        self.collection_name = collection_name
        self.collection = self.db_conn[f"{collection_name}s_collection"]

    def get_one(self, filters: dict) -> tuple[bool, dict]:
        """
        Retrieve a single record from the collection based on the given filters.
        Args:
            filters (dict): A dictionary specifying the filters to apply.
        Returns:
            tuple[bool, dict]: A tuple containing a boolean value indicating whether
            a record exists and the record itself, if it exists.
        """
        record = self.collection.find_one(filters, {"_id": 0})
        record_exists = record is not None
        return record_exists, record

    def get_all(self, filters: dict) -> GridOutCursor:
        """
        Retrieve all records from the collection based on the given filters.
        Args:
            filters (dict): A dictionary specifying the filters to apply.
        Returns:
            GridOutCursor: A cursor object containing all retrieved records.
        """
        return self.collection.find(filters)

    def save(
        self, user_data: Union[Patient, CareGiver, Professional]
    ) -> Union[None | dict]:
        """
        Save user data to the collection.
        Args:
            user_data: An instance of either Patient, CareGiver, or Professional class.
        Returns:
            dict: The dictionary representation of the saved user data, excluding the password field.
            None: If an error occurred during the save operation.
        """
        result = None
        try:
            user_data.password = self.__hash_password(passwd=user_data.password)
            self.collection.insert_one(user_data.dict())
            result = user_data.dict(exclude={"password"})
        except (PyMongoError, Exception) as save_err:
            logger.error("Error saving user data: %s", save_err)

        return result

    def retrieve_user_schema(self) -> Union[User, Patient, CareGiver, Professional]:
        """
        Retrieve the user schema based on the collection name.
        Args:
            self.collection_name (str): The name of the collection.
        Returns:
            Union[User, Patient, CareGiver, Professional]: The user schema based on the collection name.
        """
        user_model_schemas = {
            "patient": Patient,
            "caregiver": CareGiver,
            "healthcare_professional": Professional,
        }
        return user_model_schemas.get(self.collection_name, User)

    @staticmethod
    def __hash_password(passwd: str) -> str:
        return PasswordHelper.get_password_hash(passwd)
