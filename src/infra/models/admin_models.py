from uuid import uuid4

from sqlmodel import Field, SQLModel

from src.shared.mixins import PasswordMixin


class Admin(SQLModel, PasswordMixin, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(unique=True, max_length=120)
    password: str = Field(max_length=500)
    is_active: bool = Field(default=True)
