import re

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.utils.db import get_db
from utils.user_manager import UserManager

prediction_service = FastAPI(
    title="Prediction microservice",
    version="1.0.0",
)
DB_SESSION = get_db()


@prediction_service.get("/")
async def home_sweet_home(request: Request):
    return JSONResponse(
        {
            "NAME": request.app.title,
            "VERSION": request.app.version,
        }
    )


@prediction_service.get("/predict_score/{username}")
def predict_memory_score(username: str):
    """
    Predicts the memory score for a given username.
    Args:
        username (str): The username for which to predict the memory score.
    Returns:
        Dict[str, float]: A dictionary containing the predicted memory score.
    """
    user_manager = UserManager(db_conn=DB_SESSION, collection_name="patient")
    _, user = user_manager.get_one({"name": re.compile(username, re.IGNORECASE)})
    score = predict_score(user)
    return {"predicted_score": score}


def predict_score(user: dict) -> int:
    """
    Predicts the score based on the user's memory score and age.
    Args:
        user (dict): A dictionary containing the user's information.
            - memory_score (int): The user's memory score.
            - age (int): The user's age.
    Returns:
        int: The predicted score.
    """
    memory_score = user.get("memory_score")
    age = user.get("age")
    if age > 50:
        return memory_score + 5
    else:
        return memory_score + 3
