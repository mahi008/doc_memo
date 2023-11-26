from utils.db import get_db
from utils.password_helper import PasswordHelper
from utils.user_manager import UserManager

DB_SESSION = get_db()

users = [
    {
        "name": "Albertus",
        "status": "patient",
        "age": 40,
        "memory_score": 26,
    },
    {
        "name": "Violetta",
        "status": "caregiver",
        "related_patient": "Albertus",
    },
    {
        "name": "Markus",
        "status": "healthcare_professional",
        "type": "general_practitioner",
    },
    {
        "name": "Marta",
        "status": "healthcare_professional",
        "type": "neurologist",
    },
    {
        "name": "Iga",
        "status": "healthcare_professional",
        "type": "psychologist",
    },
]

try:
    for user in users:
        user_manager = UserManager(db_conn=DB_SESSION, collection_name=user["status"])
        user_schema = user_manager.retrieve_user_schema()
        print("INSERTING USER ============>", user, flush=True)
        user["password"] = "secret"
        user_manager.save(user_data=user_schema(**user))
except Exception as e:
    print("Failed to import data:", e)
