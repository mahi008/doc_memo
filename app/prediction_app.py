import re

from fastapi import FastAPI, Request, HTTPException
from starlette import status
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
    user_manager = UserManager(db_conn=DB_SESSION, collection_name="patient")
    _, user = user_manager.get_one({"name": re.compile(username, re.IGNORECASE)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    score = predict_score(user)
    return {"predicted_score": score}


def predict_score(user: dict) -> int:
    memory_score = user.get("memory_score")
    age = user.get("age")
    if age > 50:
        return memory_score + 5
    else:
        return memory_score + 3
