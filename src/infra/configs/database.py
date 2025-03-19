from os import getenv
from sqlmodel import SQLModel, create_engine



def create_tables():
    engine = create_engine(
        f"postgresql://{getenv('DB-USER')}:{getenv('DB-PASSWORD')}@{getenv('DB-HOST')}:{getenv('DB-PORT')}/{getenv('DB-NAME')}",
    echo=True)
    SQLModel.metadata.create_all(engine)
    print("Connected")
