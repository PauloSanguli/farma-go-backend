from sqlmodel import SQLModel, Field
from typing import Type
from uuid import uuid4



class User(SQLModel, table=True):
    id: str = Field(default=uuid4(), primary_key=True)
    email: str = Field(unique=True, max_length=120)
    password: str = Field(max_length=500)
    is_active: bool = Field(default=True)
