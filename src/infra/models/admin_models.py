from typing import Type
from uuid import uuid4

from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel import UUID, Field, Relationship, SQLModel

from src.domain.security import check_password_hashed, hash_password
from src.infra.models.pharmacy_models import Pharmacy

from src.shared.mixins import PasswordMixin


class Admin(SQLModel, PasswordMixin, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(unique=True, max_length=120)
    password: str = Field(max_length=500)
    is_active: bool = Field(default=True)

    # updated_pharmacies: list["Pharmacy"] = Relationship(
    #     back_populates="updated_by_admin",
    #     sa_relationship_kwargs={
    #         "primaryjoin": "Admin.id==Pharmacy.updated_by_admin_id"
    #     },
    # )

    # def _encrypt_password(self, password: str | None = None) -> None:
    #     self.password = hash_password(password or self.password)

    # def _check_password(self, password: str | None) -> bool:
    #     if not check_password_hashed(password, self.password):
    #         raise HTTPException(
    #             detail=""
    #         )
    #     return check_password_hashed(password, self.password)
