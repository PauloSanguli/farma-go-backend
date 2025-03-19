# from sqlmodel import SQLModel
# from sqlmodel import Field

# from datetime import datetime

# from uuid import uuid4



# class BaseModel(SQLModel, table=True):
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)

# class AuthModel(BaseModel, table=True):
#     name: str = Field(max_length=100, index=True)
#     password: str = Field(max_length=255)
#     email: str = Field(unique=True, max_length=100)
