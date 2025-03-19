from uuid import uuid4
from typing import Type, Optional
from sqlmodel import SQLModel, Field, Relationship

from .base_model import BaseModel


class User(BaseModel):
    name: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=100)
    password_hash: str = Field(max_length=255)
    role: str = Field(default="pharmacist", max_length=20)
    # pharmacy_id: Optional[str] = Field(default=None, foreign_key="pharmacy.id")

    # pharmacy: Optional[Pharmacy] = Relationship()
