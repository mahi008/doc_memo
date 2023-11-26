from unittest.mock import MagicMock, patch

import pytest


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
def mock_user_patient():
    return {
        "name": "John",
        "password": "Doe",
        "status": "patient",
        "age": 55,
        "memory_score": 45,
    }


@pytest.fixture
def mock_user_caregiver():
    return {
        "name": "Jane",
        "password": "Doe",
        "status": "caregiver",
        "related_patients": "John",
    }


@pytest.fixture
def mock_user_professional():
    return {
        "name": "Mickey",
        "password": "mouse",
        "status": "healthcare_professional",
        "type": "general_practitioner",
    }
