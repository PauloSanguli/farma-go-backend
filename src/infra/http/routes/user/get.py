from fastapi import APIRouter

from src.infra.http.controllers import UserController

from typing import Annotated

from fastapi import Depends

from src.infra.http.middleware.authorizators import JWTPermissionsHandler

app = APIRouter(prefix="/user", tags=["User"])

@app.get("/search-medicine/")
async def search_medicine(
    user_logged: Annotated[dict[str, str], Depends(JWTPermissionsHandler.get_user_logged)],
    medicine: str
):
    results: list = UserController.search_medicine_in_pharmacy_stock(medicine)
    return results