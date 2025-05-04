from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.infra.http.repositorys import AdminRepository
from src.infra.models import AddressPharmacy, Pharmacist, Pharmacy

app = APIRouter(prefix="/admin")


@app.get("/pharmacy")
async def list_pharmacys():
    return AdminRepository.list_pharmacys()
