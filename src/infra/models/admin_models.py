from sqlmodel import SQLModel, Field
from typing import Type
from uuid import uuid4

from .base_model import BaseModel


class Admin(BaseModel):
    email: str = Field(unique=True, max_length=120)
    password: str = Field(max_length=500)
    is_active: bool = Field(default=True)
