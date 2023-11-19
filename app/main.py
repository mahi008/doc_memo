from typing import Optional, Union

from fastapi import FastAPI, Request, Depends, status, HTTPException
import pymongo
from pydantic import ValidationError

from utils.db import get_db
from models import User, Patient, CareGiver, Professional, LoginInput
from utils.password_helper import PasswordHelper
from utils.user import UserManager

app = FastAPI()
DB_SESSION = get_db()


@app.get("/")
def read_root():
    client = pymongo.MongoClient(
        "mongodb://admin:root@mongodb_container:27017/?authSource=admin"
    )
    db = client.user
    users_collection = db.users_collection
    users_collection.insert_one({"username": "toto", "password": "tata"})
    return {"Hello": "World"}


@app.post("/user")
async def create_user(data: Request):
    user = await data.json()
    user_type = user.get("status")
    user_model_schema = User

    if user_type == "patient":
        user_model_schema = Patient
    if user_type == "caregiver":
        user_model_schema = CareGiver
    if user_type == "healthcare_professional":
        user_model_schema = Professional

    try:
        user_model = user_model_schema(**user)
        user_manager = UserManager(
            db_conn=DB_SESSION, collection_name=user_model.status
        )
        exist, _ = user_manager.fetch_one(
            filter={"name": user_model.name, "status": user_model.status}
        )
        if exist:
            return "User already exist"
        sv = user_manager.save(user_data=user_model)
        return sv
    except ValidationError as error:
        return error.errors()


@app.get("/patients")
def get_patients_count(mem_score_gt: int = 0, age_lt: int = 150, age_gt: int = 0):
    user_manager = UserManager(db_conn=DB_SESSION, collection_name="patient")
    s = user_manager.collection.find(
        {
            "memory_score": {"$gt": mem_score_gt},
            "$or": [{"age": {"$gt": age_gt}}, {"age": {"$lt": age_lt}}],
        }
    )
    for i in s:
        print(i)


@app.post("/login", status_code=200)
def login(login_data: LoginInput):
    user_manager = UserManager(db_conn=DB_SESSION, collection_name=login_data.status)
    _, user = user_manager.fetch_one({"name": login_data.user_name})
    verify_password = PasswordHelper.verify_password(
        login_data.password, user.get("password")
    )
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Verify your username/password",
        )
    return {"login": "successful !"}
