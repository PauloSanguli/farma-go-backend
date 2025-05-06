from pydantic import BaseModel, EmailStr


class AuthSchema(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserUpdateSchema(BaseModel):
    email: EmailStr
    name: str
