from typing import Annotated

from uuid import uuid4

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi import Depends

from src.domain.schemas import AuthSchema, PharmacistSchema, PharmacySchema, AddressPharmacySchema
from src.infra.models import Medicine, Pharmacy, AddressPharmacy
from src.infra.http.controllers import PharmacyController
from src.infra.http.repositorys import PharmacyRepository
from src.infra.http.middleware.authorizators import JWTPermissionsHandler


app = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])



@app.get("/retrieve/", response_model=PharmacySchema)
async def retrieve_pharmacy(
    pharmacist_logged: Annotated[dict[str, str], Depends(JWTPermissionsHandler.get_pharmacist_logged)]
):
    result: dict = PharmacyRepository.retrieve_pharmacy_by_id(pharmacist_logged.get("tennant"))
    pharmacy: Pharmacy = result.get("pharmacy")
    address: AddressPharmacy = result.get("address")
    address_dict = address.model_dump() if hasattr(address, 'model_dump') else address.__dict__

    return PharmacySchema(
        id=pharmacy.id,
        name=pharmacy.name,
        phone=pharmacy.phone,
        opened=pharmacy.opened,
        opening_hours=pharmacy.opening_hours,
        # image_url=pharmacy.image_url,
        address=AddressPharmacySchema.model_validate(address_dict),
        created_at=pharmacy.created_at
    )

