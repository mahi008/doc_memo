from typing import Optional, Union

from fastapi import FastAPI
import pymongo

from models import User, Patient, Professional, CareGiver

app = FastAPI()


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
def create_user(data: User):
    res = None
    print(data.status.age)
    pass
