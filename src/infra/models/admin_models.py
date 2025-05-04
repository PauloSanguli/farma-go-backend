from typing import Type
from uuid import uuid4

from sqlmodel import UUID, Field, Relationship, SQLModel

from src.infra.models.pharmacy_models import Pharmacy


class Admin(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(unique=True, max_length=120)
    password: str = Field(max_length=500)
    is_active: bool = Field(default=True)

    updated_pharmacies: list["Pharmacy"] = Relationship(
        back_populates="updated_by_admin",
        sa_relationship_kwargs={
            "primaryjoin": "Admin.id==Pharmacy.updated_by_admin_id"
        },
    )
