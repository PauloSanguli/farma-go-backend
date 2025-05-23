from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.domain.schemas import MedicinestockSchema
from src.infra.http.controllers import PharmacyController
from src.infra.http.middleware.authorizators import JWTPermissionsHandler
from src.infra.http.repositorys import PharmacyRepository
from src.infra.models import AddressPharmacy, Medicine, Pharmacy

app = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])


@app.patch("/medicine")
def update_stock(
    pharmacist_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_pharmacist_logged)
    ],
    medicine: MedicinestockSchema,
):
    response = PharmacyController.update_medicine_stock(
        medicine, pharmacist_logged.get("tennant")
    )
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)
