from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import create_engine

from .database import create_tables

api = FastAPI()


@api.on_event("startup")
def on_startup():
    load_dotenv()
    create_tables()
