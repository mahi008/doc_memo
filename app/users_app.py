from typing import Dict, List, Union

import httpx
from fastapi import FastAPI, HTTPException, Request, status
from pydantic import ValidationError
from starlette.responses import JSONResponse

from models.user import LoginInput
from utils.db import get_db
from utils.password_helper import PasswordHelper
from utils.user_manager import UserManager

users_service = FastAPI(
    title="Users microservice",
    version="1.0.0",
)
DB_SESSION = get_db()


@users_service.get("/")
async def home_sweet_home(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "NAME": request.app.title,
            "VERSION": request.app.version,
        }
    )


@users_service.post("/user")
async def create_user(data: Request) -> Union[Dict[str, str], List[Dict[str, str]]]:
    """
    Create a new user.
    Args:
        data (Request): The request object containing the user data.
    Returns:
        Union[Dict[str, str], List[Dict[str, str]]]: The response indicating the success
        or failure of the user creation.
    """
    user = await data.json()
    user_type = user.get("status")
    user_manager = UserManager(db_conn=DB_SESSION, collection_name=user_type)
    user_model_schema = user_manager.retrieve_user_schema()

    try:
        user_model = user_model_schema(**user)
        user_exist, _ = user_manager.get_one(
            filters={"name": user_model.name, "status": user_model.status}
        )
        # Can't create a user that already exists
        if user_exist:
            return {"error": "User already exists"}
        return user_manager.save(user_data=user_model)
    except ValidationError as validation_err:
        raise HTTPException(status_code=422, detail=str(validation_err))
    except Exception as other_err:
        raise HTTPException(status_code=500, detail=str(other_err))


@users_service.get("/patient")
def get_patients_count(
    mem_score_gt: int = 0, age_gt: int = 0, age_lt: int = 150
) -> dict:
    """
    Get the count of patients based on memory score and age filters.

    Args:
        mem_score_gt (int): Minimum memory score. Default is 0.
        age_gt (int): Minimum age. Default is 0.
        age_lt (int): Maximum age. Default is 150.

    Returns:
        dict: A dictionary containing the count of patients.
    """
    user_manager = UserManager(DB_SESSION, collection_name="patient")
    count_query = {
        "memory_score": {"$gt": mem_score_gt},
        "age": {"$gt": age_gt, "$lt": age_lt},
    }
    count = user_manager.collection.count_documents(count_query)
    return {"count": count}


@users_service.get("/patient/{username}/score")
def get_prediction_score(username: str) -> dict:
    """
    Get the prediction score for a patient.
    Args:
        username (str): The username of the patient.
    Returns:
        dict: The prediction score for the patient.
    Raises:
        HTTPException: If the prediction service is not available.
    """
    error_msg = None
    prediction_uri = f"http://doc_memo-prediction_app-1:8000/predict_score/{username}"
    result = None
    try:
        req = httpx.get(prediction_uri)
        req.raise_for_status()
        result = req.json()
    except httpx.HTTPError as http_error:
        error_msg = http_error
    except httpx.RequestError as req_error:
        error_msg = req_error

    if error_msg:
        return {"error": error_msg}

    return result


@users_service.post("/login", status_code=200)
def login(login_data: LoginInput) -> dict:
    """
    Handle user login.
    Args:
        login_data (LoginInput): The login data containing the user's credentials.
    Returns:
        dict: A dictionary indicating the success or failure of the login.
    """
    user_manager = UserManager(db_conn=DB_SESSION, collection_name=login_data.status)
    user_exist, user = user_manager.get_one(
        filters={"name": login_data.user_name.lower()}
    )
    if (not user_exist and not user) or not PasswordHelper.verify_password(
        login_data.password, user.get("password")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Verify your username/password",
        )
    return {"login": "successful!"}
