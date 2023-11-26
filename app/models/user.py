from typing import Literal

from pydantic import BaseModel, constr, Extra


class User(BaseModel):
    name: constr(to_lower=True)
    password: str
    status: Literal["patient", "caregiver", "healthcare_professional"]


class Patient(User):
    age: int
    memory_score: int


class CareGiver(User):
    related_patient: str

    class Config:
        extra = Extra.ignore


class Professional(User):
    type: Literal["general_practitioner", "neurologist", "psychologist"]

    class Config:
        extra = Extra.ignore


class LoginInput(BaseModel):
    user_name: str
    password: str
    status: Literal["patient", "caregiver", "healthcare_professional"]
