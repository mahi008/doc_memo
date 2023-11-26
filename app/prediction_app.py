from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from utils.db import get_db
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
def get_prediction_score(username: str):
    """
    Get the prediction score for a given username.
    Args:
        username (str): The username of the user to get the prediction score for.
    Returns:
        dict: A dictionary containing the predicted score.
            If the user is not found, an error message is returned.
    """
    user_manager = UserManager(db_conn=DB_SESSION, collection_name="patient")
    user_exists, user = user_manager.get_one({"name": username})
    if not user_exists:
        return {"error": "User not found"}
    score = predict_score(user)
    return {"predicted_score": score}


def predict_score(user: dict) -> int:
    """
    Predicts the score based on the user's memory score and age.
    Args:
        user (dict): Dictionary containing user information.
    Returns:
        int: Predicted score.
    """
    memory_score = user.get("memory_score")
    age = user.get("age")
    score = None
    if age and age > 50:
        score = memory_score + 5
    if age and age < 50:
        score = memory_score + 3

    return score
