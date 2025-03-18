from sqlmodel import SQLModel, Field, ForeignKey
from uuid import uuid4
from datetime import datetime
from typing import Optional

from .base_model import BaseModel



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


class PharmacyImage(BaseModel):
    pharmacy_id: str = Field(foreign_key="pharmacy.id")
    image_url: str = Field(max_length=255)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
