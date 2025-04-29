from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AddressPharmacySchema(BaseModel):
    street: str
    neighborhood: str
    city: str
    state: str
    zip_code: str
    latitude: Optional[float]
    longitude: Optional[float]


class PharmacySchema(BaseModel):
    name: str
    phone: Optional[str]
    opened: bool
    opening_hours: Optional[str]
    image_url: Optional[str]
    address: AddressPharmacySchema
    pharmacist_id: str
