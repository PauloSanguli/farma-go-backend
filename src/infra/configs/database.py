from os import getenv

from sqlmodel import Session, SQLModel, create_engine


def create_tables():
    engine = get_engine_connection()
    SQLModel.metadata.create_all(engine)


def get_engine_connection():
    engine = create_engine(
        f"postgresql://{getenv('DB-USER')}:{getenv('DB-PASSWORD')}@{getenv('DB-HOST')}:{getenv('DB-PORT')}/{getenv('DB-NAME')}",
        # echo=True,
    )
    return engine


def get_session():
    engine = get_engine_connection()
    with Session(engine) as session:
        return session
