from typing import Annotated

from uuid import uuid4

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi import Depends

from src.domain.schemas import AuthSchema, PharmacistSchema, PharmacySchema, AddressPharmacySchema
from src.infra.models import Medicine, Pharmacy, AddressPharmacy, Stock
from src.infra.http.controllers import UserController
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
