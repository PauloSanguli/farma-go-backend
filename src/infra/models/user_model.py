from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.domain.security import hash_password
from src.shared.mixins import PasswordMixin


class User(SQLModel, PasswordMixin, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    name: str = Field(
        max_length=100,
        index=True,
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    password: str = Field(max_length=500)
    image_url: Optional[str] = Field(max_length=500, default=None)
    email: str = Field(unique=True, max_length=120)

    search_history: List["UserSearchHistory"] = Relationship(back_populates="user")


class UserSearchHistory(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    query: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="search_history")
