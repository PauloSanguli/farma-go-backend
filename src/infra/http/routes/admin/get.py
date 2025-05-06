from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.infra.http.middleware.authorizators import JWTPermissionsHandler
from src.infra.http.repositorys import AdminRepository
from src.infra.models import AddressPharmacy, Pharmacist, Pharmacy

app = APIRouter(prefix="/admin", tags=["Admin"])


@app.get("/pharmacy")
async def list_pharmacys(
    admin_logged: Annotated[dict, Depends(JWTPermissionsHandler.get_admin_logged)],
):
    return AdminRepository.list_pharmacys()
