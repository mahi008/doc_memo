import re

from fastapi import FastAPI

from utils.db import get_db
from utils.user import UserManager

app = FastAPI()
DB_SESSION = get_db()


@app.get("/")
def home_sweet_home():
    return {"Prediction": "1"}


@app.get("/predict_score/{user_name}")
def predict_memory_score(user_name: str):
    user_manager = UserManager(db_conn=DB_SESSION, collection_name="patient")
    _, user = user_manager.fetch_one({"name": re.compile(user_name, re.IGNORECASE)})
    score = predict_score(user)
    return {"predicted_score": score}


def predict_score(user: dict) -> int:
    mem_score = user.get("memory_score")
    return mem_score + 5 if user.get("age") > 50 else mem_score + 3
