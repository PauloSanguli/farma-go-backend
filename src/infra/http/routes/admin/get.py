from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

# from src.infra.http.middleware.dependencie_admin import JWTTokenExceptionHandler
from src.infra.http.repositorys import AdminRepository
from src.infra.models import AddressPharmacy, Pharmacist, Pharmacy

app = APIRouter(prefix="/admin", tags=["Admin"])


@app.get("/pharmacy")
async def list_pharmacys(
    # admin_logged: Annotated[dict, Depends(JWTTokenExceptionHandler.get_user_logged)],
):
    return AdminRepository.list_pharmacys()
