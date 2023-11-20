from typing import Union

from models import Patient, CareGiver, Professional
from utils.password_helper import PasswordHelper


class UserManager:
    collection = None
    db_conn = None

    def __init__(self, db_conn, collection_name):
        self.db_conn = db_conn
        self.collection = self.db_conn[f"{collection_name}s_collection"]

    def fetch_one(self, filter: dict) -> tuple[bool, dict]:
        tt = self.collection.find_one(filter, {"_id": 0})
        print("tt ============>", tt, flush=True)
        return tt is not None, tt

    def fetch(self, filter):
        return self.collection.find()

    def filter(self, filter):
        pass

    def save(self, user_data: Union[Patient, CareGiver, Professional]) -> dict:
        user_data.password = self.__hash_password(passwd=user_data.password)
        self.collection.insert_one(user_data.dict())
        return user_data.dict(exclude={"password"})

    @staticmethod
    def __hash_password(passwd: str) -> str:
        return PasswordHelper.get_password_hash(passwd)

    pass
