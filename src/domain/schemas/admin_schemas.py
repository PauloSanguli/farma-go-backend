from pydantic import BaseModel, EmailStr



class AdminSchema(BaseModel):
    email: EmailStr
    password: str
