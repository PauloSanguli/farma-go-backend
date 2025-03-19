from uuid import uuid4
from typing import Type, Optional
from sqlmodel import SQLModel, Field, Relationship

from .base_model import AuthModel

from src.domain.enums import UserRole


class User(AuthModel):
    role: str = Field(sa_column_kwargs={"nullable": False}, default=UserRole.User)
