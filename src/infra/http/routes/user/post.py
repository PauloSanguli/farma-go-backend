from typing import Annotated

from uuid import uuid4

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi import Depends

from src.domain.schemas import AuthSchema, UserSchema
from src.infra.models import Medicine, Pharmacy, AddressPharmacy, Stock, User
from src.infra.http.controllers import UserController
from src.infra.http.repositorys.user_repository import UserRepository
from src.infra.http.middleware.authorizators import JWTPermissionsHandler


app = APIRouter(prefix="/user", tags=["User"])

@app.post("/login")
def user_login(user_data: AuthSchema):
    token: str = UserController.authenticate_user(user_data)
    return JSONResponse(
        content={
            "token": token
        },
        status_code=status.HTTP_201_CREATED
    )

@app.post("/")
def create_user(user: UserSchema):
    response: dict = UserRepository.create_user(user)
    return JSONResponse(
        content=response,
        status_code=status.HTTP_201_CREATED
    )
