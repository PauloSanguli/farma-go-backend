from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.infra.http.middleware.authorizators import JWTPermissionsHandler
from src.infra.http.repositorys import AdminRepository
from src.infra.models import AddressPharmacy, Pharmacist, Pharmacy

app = APIRouter(prefix="/admin", tags=["Admin"])


@app.delete("/pharmacy")
def remove_pharmacy(
    admin_logged: Annotated[dict, Depends(JWTPermissionsHandler.get_admin_logged)],
    uuid: str,
):
    return AdminRepository.delete_pharmacy(pharmacy_id=uuid)
