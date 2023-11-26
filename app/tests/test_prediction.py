from unittest.mock import patch

from fastapi.testclient import TestClient

from prediction_app import prediction_service

client = TestClient(prediction_service)


def test_home_page():
    request = client.get("/")
    assert request.status_code == 200
    # with pytest.raises(HTTPException) as exc_info:


@patch("users_app.UserManager.get_one")
def test_valid_prediction(mock_get_one, mock_user_patient):
    """
    Test case valid prediction
    """
    mock_get_one.return_value = (True, mock_user_patient)
    response = client.get(f"/predict_score/{mock_user_patient['name']}")
    assert response.status_code == 200
    assert response.json().get("predicted_score") == 50


@patch("users_app.UserManager.get_one")
def test_invalid_prediction(user_manager_get_one_mock):
    """
    Test case invalid prediction
    """
    user_manager_get_one_mock.return_value = False, None
    request = client.get(f"/predict_score/toto")
    assert request.status_code == 200
    assert request.json() == {"error": "User not found"}
