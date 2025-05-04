from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.infra.http.repositorys import AdminRepository
from src.infra.models import AddressPharmacy, Pharmacist, Pharmacy

app = APIRouter(prefix="/admin", tags=["Admin"])


@app.delete("/pharmacy")
def remove_pharmacy(uuid: str):
    return AdminRepository.delete_pharmacy(pharmacy_id=uuid)
