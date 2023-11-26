from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from requests import Response

from users_app import users_service
from utils.password_helper import PasswordHelper

client = TestClient(users_service)


def test_home_page():
    request = client.get("/")
    assert request.status_code == 200


@patch("users_app.UserManager.get_one")
@patch("users_app.UserManager.save")
def test_create_user_success(
    user_manager_save_mock,
    user_manager_get_one_mock,
    mock_user_patient,
):
    """
    Test case for successfully creating a user.
    """
    user_manager_get_one_mock.return_value = False, None
    user_manager_save_mock.return_value = mock_user_patient
    request = client.post("/user", json=mock_user_patient)
    assert request.json() == mock_user_patient
    assert request.status_code == 200


def test_create_user_missing_data(mock_user_patient):
    """
    Test case for creating a user with a missing data.
    """
    del mock_user_patient["name"]
    request = client.post("/user", json=mock_user_patient)
    assert request.status_code == 422


def test_create_user_with_invalid_status(mock_user_patient):
    """
    Test case for creating a user with a missing data.
    """
    mock_user_patient["status"] = "my_invalid_status"
    request = client.post("/user", json=mock_user_patient)
    assert request.status_code == 422


@patch("users_app.UserManager.get_one")
def test_successful_login(user_manager_get_one_mock, mock_user_patient):
    """
    Test case for successful login
    """
    user_in_db = mock_user_patient.copy()
    user_in_db["password"] = PasswordHelper.get_password_hash(user_in_db["password"])
    user_manager_get_one_mock.return_value = True, user_in_db
    request = client.post(
        "/login",
        json={
            "user_name": mock_user_patient["name"],
            "password": mock_user_patient["password"],
            "status": mock_user_patient["status"],
        },
    )
    assert request.status_code == 200
    assert request.json() == {"login": "successful!"}


@patch("users_app.UserManager.get_one")
def test_invalid_login(user_manager_get_one_mock, mock_user_patient):
    """
    Test case for invalid login
    """
    user_in_db = mock_user_patient
    user_in_db["password"] = PasswordHelper.get_password_hash(user_in_db["password"])
    user_manager_get_one_mock.return_value = True, user_in_db
    request = client.post(
        "/login",
        json={
            "user_name": mock_user_patient["name"],
            "password": mock_user_patient["password"],
            "status": mock_user_patient["status"],
        },
    )
    assert request.status_code == 401


@patch("users_app.httpx.get")
def test_prediction(api_mock, mock_user_patient):
    """
    Test case for prediction
    """
    the_response = Mock(spec=Response)
    the_response.status_code = 200
    api_mock.return_value = the_response
    the_response.json.return_value = {"prediction": 50}

    request = client.get(
        f"/patient/{mock_user_patient['name']}/score",
    )
    assert request.status_code == 200
