from typing import Annotated

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi import Depends

from src.domain.schemas import AuthSchema, PharmacistSchema
from src.infra.models import Medicine
from src.infra.http.controllers import PharmacyController
from src.infra.http.repositorys import PharmacyRepository
from src.infra.http.middleware.authorizators import JWTPermissionsHandler


app = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])


@app.post("/medicine")
def regist_medicine(
    pharmacist_logged: Annotated[dict[str, str], Depends(JWTPermissionsHandler.get_pharmacist_logged)],
    medicine: Medicine):
    response: dict[str, str] = PharmacyRepository.regist_medicine(medicine, pharmacist_logged.get("tennant"))
    return JSONResponse(
        content=response,
        status_code=status.HTTP_201_CREATED,
    )

@app.post("/pharmacist/login")
def pharmacist_login(pharmacist: AuthSchema):
    response: dict[str, str] = PharmacyController.authenticate_pharmacist(pharmacist)
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
