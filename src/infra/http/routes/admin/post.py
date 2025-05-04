from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

from src.infra.http.repositorys import AdminRepository

from src.infra.models import Pharmacy, Pharmacist, AddressPharmacy


app = APIRouter(prefix="/admin")


@app.post("/pharmacy")
async def regist_pharmacy(
    pharmacy: Pharmacy, address: AddressPharmacy, pharmacist: Pharmacist
):
    response = AdminRepository.regist_pharmacy(pharmacy, address, pharmacist)
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
