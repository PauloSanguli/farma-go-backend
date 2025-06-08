from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.domain.enums import MedicineCategory
from src.shared.mixins import PasswordMixin


class AddressPharmacy(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    street: Optional[str] = Field(max_length=100)
    neighborhood: Optional[str] = Field(max_length=100)
    city: Optional[str] = Field(max_length=100)
    state: Optional[str] = Field(max_length=50)
    zip_code: str = Field(max_length=20)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)

    pharmacy: Optional["Pharmacy"] = Relationship(back_populates="address")

        


class PharmacyImage(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    pharmacy_id: str = Field(foreign_key="pharmacy.id")
    image_url: str = Field(max_length=500)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    pharmacy: Optional["Pharmacy"] = Relationship(back_populates="pharmacy_images")


class Pharmacist(SQLModel, PasswordMixin, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    name: str = Field(max_length=100, index=True)
    password: str = Field(max_length=500)
    email: str = Field(
        unique=True,
        max_length=120,
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    phone: Optional[str] = Field(
        max_length=20,
        regex=r"^\+?\d{1,4}?[-.\s]?(\(?\d{1,4}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{4,9}$",
    )
    license_number: str = Field(max_length=50, unique=True)

    pharmacy_id: str = Field(foreign_key="pharmacy.id")
    pharmacy: Optional["Pharmacy"] = Relationship(back_populates="pharmacists")


class Pharmacy(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    name: str = Field(max_length=100, index=True)
    phone: Optional[str] = Field(
        max_length=20,
        default=None,
        regex=r"^\+?\d{1,4}?[-.\s]?(\(?\d{1,4}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{4,9}$",
    )
    opened: bool = Field(default=False)
    opening_hours: Optional[str] = Field(default=None)

    pharmacy_images: List["PharmacyImage"] = Relationship(back_populates="pharmacy")

    address_id: str = Field(foreign_key="addresspharmacy.id")
    address: "AddressPharmacy" = Relationship(back_populates="pharmacy")

    stock_id: Optional[str] = Field(foreign_key="stock.id")
    stock: Optional["Stock"] = Relationship(back_populates="pharmacy")

    pharmacists: List["Pharmacist"] = Relationship(back_populates="pharmacy")


class Stock(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    pharmacy: Pharmacy = Relationship(back_populates="stock")

    medicines: List["Medicine"] = Relationship(back_populates="stock")


class Medicine(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    name: str = Field(max_length=100, index=True)
    description: Optional[str] = Field(default=None, max_length=255)
    price: float = Field(gt=0)
    category: MedicineCategory = Field(sa_column_kwargs={"nullable": False})
    image_url: Optional[str] = Field(
        sa_column_kwargs={"nullable": True}, max_length=255
    )

    quantity: int = Field(default=1)

    stock_id: str = Field(foreign_key="stock.id")
    stock: Optional["Stock"] = Relationship(back_populates="medicines")
