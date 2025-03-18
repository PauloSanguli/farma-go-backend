from sqlmodel import SQLModel
from sqlmodel import Field

from uuid import uuid4



class BaseModel(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
