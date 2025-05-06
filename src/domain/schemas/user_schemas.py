from pydantic import BaseModel, EmailStr


class AuthSchema(BaseModel):
    email: EmailStr
    password: str
