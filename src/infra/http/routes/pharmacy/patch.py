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
