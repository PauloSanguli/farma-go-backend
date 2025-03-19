from uuid import uuid4
from typing import Type, Optional
from sqlmodel import SQLModel, Field, Relationship

from src.domain.enums import UserRole

from datetime import datetime



class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    role: str = Field(sa_column_kwargs={"nullable": False}, default=UserRole.USER)
    name: str = Field(max_length=100, index=True)
    password: str = Field(max_length=255)
    email: str = Field(unique=True, max_length=100)