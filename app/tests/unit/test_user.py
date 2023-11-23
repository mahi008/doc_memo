import pytest
from unittest.mock import MagicMock, AsyncMock

from users_app import create_user


@pytest.fixture
def mock_data():
    return MagicMock()


@pytest.fixture
def mock_user_manager():
    return MagicMock()


@pytest.fixture
def mock_user_model_schema():
    return MagicMock()


@pytest.fixture
def mock_user():
    return {"name": "John", "status": "patient"}


@pytest.mark.asyncio
async def test_create_user_success(
    mock_data, mock_user_manager, mock_user_model_schema, mock_user
):
    # Mock dependencies
    mock_data.json.return_value = mock_user
    mock_user_manager.retrieve_user_schema.return_value = mock_user_model_schema
    mock_user_manager.save.return_value = {"success": "User created"}

    # Call the function
    response = await create_user(mock_data)

    # Check the response
    assert response == {"success": "User created"}


@pytest.mark.asyncio
async def test_create_user_user_exists(
    mock_data, mock_user_manager, mock_user_model_schema, mock_user
):
    # Mock dependencies
    mock_data.json.return_value = mock_user
    mock_user_manager.retrieve_user_schema.return_value = mock_user_model_schema
    mock_user_manager.get_one.return_value = True, None

    # Call the function
    response = await create_user(mock_data)

    # Check the response
    assert response == {"error": "User already exists"}


@pytest.mark.asyncio
async def test_create_user_validation_error(
    mock_data, mock_user_manager, mock_user_model_schema, mock_user
):
    # Mock dependencies
    mock_data.json.return_value = mock_user
    mock_user_manager.retrieve_user_schema.return_value = mock_user_model_schema
    mock_user_manager.get_one.return_value = False, None
    validation_error = ValidationError(errors={"name": "Invalid name"})
    mock_user_model_schema.side_effect = validation_error

    # Call the function
    response = await create_user(mock_data)

    # Check the response
    assert response == {"name": "Invalid name"}


@pytest.mark.asyncio
async def test_create_user_other_error(
    mock_data, mock_user_manager, mock_user_model_schema, mock_user
):
    # Mock dependencies
    mock_data.json.return_value = mock_user
    mock_user_manager.retrieve_user_schema.return_value = mock_user_model_schema
    mock_user_manager.get_one.return_value = False, None
    other_error = Exception("Some error")
    mock_user_model_schema.side_effect = other_error

    # Call the function
    response = await create_user(mock_data)

    # Check the response
    assert response == {"error": "Some error"}
