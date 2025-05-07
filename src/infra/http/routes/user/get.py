from fastapi import APIRouter

from src.infra.http.controllers import UserController
from src.infra.http.repositorys import UserRepository

from typing import Annotated

from fastapi import Depends

from src.infra.http.middleware.authorizators import JWTPermissionsHandler
from src.domain.schemas import UserSchema
from src.infra.models import User

app = APIRouter(prefix="/user", tags=["User"])

@app.get("/search-medicine/")
async def search_medicine(
    user_logged: Annotated[dict[str, str], Depends(JWTPermissionsHandler.get_user_logged)],
    medicine: str,
    lat: float,
    lg: float
):
    results: list = UserController.search_medicine_in_pharmacy_stock(medicine, user_logged.get("id"))
    return results

@app.get("/", response_model=UserSchema)
async def retrieve_profile_info(
    user_logged: Annotated[dict[str, str], Depends(JWTPermissionsHandler.get_user_logged)]
):
    user: User = UserRepository.retrieve_profile_info(user_logged.get("id"))
    return user

@app.get("/search-history/")
async def retrieve_user_history_search(
    user_logged: Annotated[dict[str, str], Depends(JWTPermissionsHandler.get_user_logged)]
):
    user: User = UserRepository.retrieve_profile_info(user_logged.get("id"))
    return user.search_history
