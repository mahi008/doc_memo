from pydantic import BaseModel, SecretStr
from typing import Literal


class User(BaseModel):
    name: str
    password: SecretStr
    status: Literal["patient", "caregiver", "healthcare_professional"]


class Patient(User):
    age: int
    memory_score: int


class CareGiver(User):
    related_patient: Patient


class Professional(User):
    type: Literal["general_practitioner", "neurologist", "psychologist"]
