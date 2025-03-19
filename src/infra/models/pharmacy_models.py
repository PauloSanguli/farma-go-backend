from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship

from .base_model import BaseModel, AuthModel

from src.domain.enums import MedicineCategory



class AddressPharmacy(BaseModel):
    street: str = Field(max_length=100)
    neighborhood: str = Field(max_length=100)
    city: str = Field(max_length=100)
    state: str = Field(max_length=50)
    zip_code: str = Field(max_length=20)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)


class Pharmacy(BaseModel):
    name: str = Field(max_length=100, index=True)
    phone: Optional[str] = Field(max_length=20, default=None)
    opened: bool = Field(default=False)
    opening_hours: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    address_id: str = Field(foreign_key="addresspharmacy.id")
    image_url: Optional[str] = Field(default=None)
    medicines: list["Medicine"] = Relationship(back_populates="pharmacy")


class PharmacyImage(BaseModel):
    pharmacy_id: str = Field(foreign_key="pharmacy.id")
    image_url: str = Field(max_length=255)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class Medicine(BaseModel):
    name: str = Field(max_length=100, index=True)
    description: Optional[str] = Field(default=None, max_length=255)
    price: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    category: MedicineCategory = Field(sa_column_kwargs={"nullable": False})  
    image_url: Optional[str] = Field(default=None, max_length=255)
    pharmacy_id: str = Field(foreign_key="pharmacy.id")

    pharmacy: Pharmacy = Relationship(back_populates="medicines")


class Pharmacist(AuthModel):
    name: str = Field(max_length=100, index=True)
    email: str = Field(max_length=100, unique=True)
    phone: Optional[str] = Field(max_length=20)
    license_number: str = Field(max_length=50, unique=True)
    pharmacy_id: str = Field(foreign_key="pharmacy.id")

    pharmacy: Pharmacy = Relationship()
