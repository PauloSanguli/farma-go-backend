from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.infra.http.middleware.authorizators import JWTPermissionsHandler
from src.infra.http.repositorys import AdminRepository
from src.infra.http.repositorys.pharmacy_repository import PharmacyRepository
from src.infra.models import AddressPharmacy, Pharmacist, Pharmacy

from src.domain.schemas import PharmacySchema, AddressPharmacySchema


app = APIRouter(prefix="/admin", tags=["Admin"])


@app.get("/pharmacy")
async def list_pharmacys(
    admin_logged: Annotated[dict, Depends(JWTPermissionsHandler.get_admin_logged)],
):
    return AdminRepository.list_pharmacys()

@app.get("/pharmacist")
async def list_pharmacists(
    admin_logged: Annotated[dict, Depends(JWTPermissionsHandler.get_admin_logged)],
):
    return AdminRepository.list_pharmacists()



@app.get("/pharmacy/retrieve/", response_model=PharmacySchema)
async def retrieve_pharmacy(
    admin_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_admin_logged)
    ],
    id: str
):
    result: dict = PharmacyRepository.retrieve_pharmacy_by_id(
        id
    )
    pharmacy: Pharmacy = result.get("pharmacy")
    address: AddressPharmacy = result.get("address")
    address_dict = (
        address.model_dump() if hasattr(address, "model_dump") else address.__dict__
    )

    return PharmacySchema(
        id=pharmacy.id,
        name=pharmacy.name,
        phone=pharmacy.phone,
        opened=pharmacy.opened,
        opening_hours=pharmacy.opening_hours,
        # image_url=pharmacy.image_url,
        address=AddressPharmacySchema.model_validate(address_dict),
        created_at=pharmacy.created_at,
    )


@app.get("/pharmacist/retrieve")
def retrieve_pharmacist(
    admin_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_admin_logged)
    ],
    id: str
):
    pharmacist = AdminRepository.retrieve_pharmacist(id)
    return pharmacist

@app.get("/total/")
def retrieve_total(
    admin_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_admin_logged)
    ]
):
    pharmacists = AdminRepository.list_pharmacists()
    pharmacy = AdminRepository.list_pharmacys()
    return JSONResponse(
        content={
            "pharmacists": len(pharmacists),
            "pharmacies": len(pharmacy),
            "active_pharmacies": len(pharmacy)
        },
        status_code=200
    )

@app.get("/export-all")
def export_all_data(
    # admin_logged: Annotated[
    #     dict[str, str], Depends(JWTPermissionsHandler.get_admin_logged)
    # ]
):
    data = AdminRepository.export_data()
    return data
