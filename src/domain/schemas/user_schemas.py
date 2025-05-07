from pydantic import BaseModel, EmailStr
from typing import Optional

class AuthSchema(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    email: EmailStr
    password: str
    name: str
    image_url: Optional[str]

class UserUpdateSchema(BaseModel):
    email: EmailStr
    name: str
