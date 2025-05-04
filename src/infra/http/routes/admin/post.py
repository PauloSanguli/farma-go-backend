from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.infra.http.repositorys import AdminRepository
from src.infra.models import AddressPharmacy, Pharmacist, Pharmacy

app = APIRouter(prefix="/admin", tags=["Admin"])


@app.post("/pharmacy")
async def regist_pharmacy(
    pharmacy: Pharmacy, address: AddressPharmacy, pharmacist: Pharmacist
):
    response: dict[str, str] = AdminRepository.regist_pharmacy(
        pharmacy, address, pharmacist
    )
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)


@app.post("/pharmacy/pharmacist")
async def regist_pharmacist_in_pharmacy(pharmacist: Pharmacist):
    response: dict[str, str] = AdminRepository.regist_pharmacist_in_pharmacy(pharmacist)
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
