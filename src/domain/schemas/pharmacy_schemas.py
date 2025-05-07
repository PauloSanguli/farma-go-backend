from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AddressPharmacySchema(BaseModel):
    street: str
    neighborhood: str
    city: str
    state: str
    zip_code: str
    latitude: Optional[float]
    longitude: Optional[float]

class CoordenatesSchema(BaseModel):
    zip_code: str
    latitude: float
    longitude: float

class PharmacySchema(BaseModel):
    name: str
    phone: Optional[str]
    opened: bool
    opening_hours: Optional[str]
    address: AddressPharmacySchema


class PharmacistSchema(BaseModel):
    created_at: datetime
    name: str
    email: str
    phone: Optional[str]
    license_number: str
    pharmacy_id: str


class MedicinestockSchema(BaseModel):
    quantity: int
    medicine_id: str
