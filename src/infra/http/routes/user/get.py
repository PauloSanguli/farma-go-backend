from typing import Annotated

from fastapi import APIRouter, Depends

from src.domain.schemas import UserSchema
from src.infra.http.controllers import UserController, PharmacyController, AdminController
from src.infra.http.middleware.authorizators import JWTPermissionsHandler
from src.infra.http.repositorys import UserRepository, AdminRepository
from src.infra.models import User, PharmacyImage, Pharmacy

app = APIRouter(prefix="/user", tags=["User"])


@app.get("/search-medicine/")
def search_medicine(
    user_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_user_logged)
    ],
    medicine: str,
    latitude: float,
    longitude: float,
):
    results: list = UserController.search_medicine_in_pharmacy_stock(
        medicine_name=medicine,
        latitude=latitude,
        longitude=longitude,
        user_id=user_logged.get("id")
    )
    pharmacy_dumped = []
    for pharmacy in results:
        pharmacy_response: dict = PharmacyController.retrieve_pharmacy_address_image(pharmacy)
        pharmacy_dumped.append(pharmacy_response)
    return pharmacy_dumped


@app.get("/", response_model=UserSchema)
def retrieve_profile_info(
    user_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_user_logged)
    ],
):
    user: User = UserRepository.retrieve_profile_info(user_logged.get("id"))
    return user


@app.get("/search-history/")
def retrieve_user_history_search(
    user_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_user_logged)
    ],
):
    response: any = UserRepository.retrieve_profile_info(user_logged.get("id"))
    return response

@app.get("/pharmacy-acessed/")
def list_pharmacys(
    user_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_user_logged)
    ]
):
    results = AdminRepository.list_pharmacys()
    pharmacy_dumped = []
    for pharmacy in results:
        pharmacy_response: dict = PharmacyController.retrieve_pharmacy_address_image(pharmacy)
        pharmacy_dumped.append(pharmacy_response)
    return pharmacy_dumped