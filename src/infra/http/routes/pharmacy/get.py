from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.domain.schemas import (
    AddressPharmacySchema,
    AuthSchema,
    PharmacistSchema,
    PharmacySchema,
)
from src.infra.http.controllers import PharmacyController
from src.infra.http.middleware.authorizators import JWTPermissionsHandler
from src.infra.http.repositorys import PharmacyRepository, AdminRepository
from src.infra.models import AddressPharmacy, Medicine, Pharmacy, Stock

app = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])


@app.get("/retrieve/", response_model=PharmacySchema)
async def retrieve_pharmacy(
    pharmacist_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_pharmacist_logged)
    ],
):
    result: dict = PharmacyRepository.retrieve_pharmacy_by_id(
        pharmacist_logged.get("tennant")
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


@app.get("/stock")
async def retrieve_pharmacy_stock(
    pharmacist_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_pharmacist_logged)
    ],
):
    result: dict = PharmacyRepository.retrieve_pharmacy_by_id(
        pharmacist_logged.get("tennant")
    )
    stock: any = result.get("medicines")
    return stock


@app.get("/search-medicine/")
async def search_medicine_in_pharmacy(
    pharmacist_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_pharmacist_logged)
    ],
    medicine: str,
):
    results: list[Pharmacy] = PharmacyController.search_medicine_in_pharmacy_stock(
        pharmacist_logged.get("tennant"), medicine
    )
    return results

@app.get("/pharmacists")
def retrieve_pharmacist(
    pharmacist_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_pharmacist_logged)
    ]
):
    AdminRepository.retrieve_pharmacist(id)
    return 