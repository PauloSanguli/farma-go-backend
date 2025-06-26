from os import getenv
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.exc import TimeoutError
from fastapi import HTTPException
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}"

# engine = create_engine(
#     DATABASE_URL,
#     pool_size=10,
#     max_overflow=5,
#     pool_timeout=30,
#     echo=False,
# )


# def create_tables():
#     SQLModel.metadata.create_all(engine)


# @contextmanager
# def get_session():
#     try:
#         with Session(engine) as session:
#             yield session
#     except TimeoutError:
#         print("Falha ao obter conexão com o banco de dados. Resetando o pool de conexões.")
#         engine.dispose()
#         # Aqui pode lançar exceção ou tratar conforme necessário



def create_tables():
    engine = get_engine_connection()
    SQLModel.metadata.create_all(engine)


def get_engine_connection():
    engine = create_engine(
        getenv("DB_URL"),
        # f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}",
        pool_size=10,
        max_overflow=5,
        pool_timeout=30,
        echo=False
    )
    return engine


def get_session():
    engine = get_engine_connection()
    with Session(engine) as session:
        return session


