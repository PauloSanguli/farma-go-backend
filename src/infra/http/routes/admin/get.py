from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.infra.http.repositorys import AdminRepository
from src.infra.models import AddressPharmacy, Pharmacist, Pharmacy

from src.infra.http.middleware.dependencie_admin import JWTTokenExceptionHandler

from typing import Annotated

app = APIRouter(prefix="/admin")


@app.get("/pharmacy")
async def list_pharmacys(admin_logged: Annotated[dict, Depends(JWTTokenExceptionHandler.get_user_logged)]):
    return AdminRepository.list_pharmacys()
