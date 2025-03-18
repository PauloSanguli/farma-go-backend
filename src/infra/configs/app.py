from fastapi import FastAPI
from .database import create_tables
from dotenv import load_dotenv

api = FastAPI()

@api.on_event("startup")
def on_startup():
    load_dotenv()
    create_tables()
