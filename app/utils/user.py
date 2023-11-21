from typing import Union

from gridfs import GridOutCursor
from models import User, Patient, CareGiver, Professional
from pymongo.errors import PyMongoError
from utils.password_helper import PasswordHelper


class UserManager:
    collection = None
    db_conn = None

    def __init__(self, db_conn, collection_name):
        self.db_conn = db_conn
        self.collection = self.db_conn[f"{collection_name}s_collection"]

    def get_one(self, filters: dict) -> tuple[bool, dict]:
        """
        Retrieve one record
        :param filters:
        :return: user dict
        """
        current_record = self.collection.find_one(filters, {"_id": 0})
        return current_record is not None, current_record

    def get_all(self, filters: dict) -> GridOutCursor:
        """
        Retrieve all records
        :param filters:
        :return:
        """
        return self.collection.find(filters)

    def save(
        self, user_data: Union[Patient, CareGiver, Professional]
    ) -> Union[None | dict]:
        """
        Save user
        :param user_data:
        :return:
        """
        result = None
        try:
            user_data.password = self.__hash_password(passwd=user_data.password)
            self.collection.insert_one(user_data.dict())
            result = user_data.dict(exclude={"password"})
        except (PyMongoError, Exception) as save_err:
            pass  # TODO: log here

        return result

    @staticmethod
    def __hash_password(passwd: str) -> str:
        """
        Has password using passlib
        :param passwd:
        :return:
        """
        return PasswordHelper.get_password_hash(passwd)

    def retrieve_user_schema(self) -> Union[User, Patient, CareGiver, Professional]:
        """
        Retrieve pydantic schema for current user type
        :param status:
        :return:
        """
        user_model_schema = User
        if self.collection == "patient":
            user_model_schema = Patient
        if self.collection == "caregiver":
            user_model_schema = CareGiver
        if self.collection == "healthcare_professional":
            user_model_schema = Professional

        return user_model_schema
