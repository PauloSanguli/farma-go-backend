import uvicorn
from dotenv import load_dotenv
from src.infra.models import (
    User,
    Pharmacist,
    Medicine,
    Pharmacy,
    PharmacyImage,
    AddressPharmacy,
)

from src.infra.http.routes.admin import app as app_admin
from src.infra.http.routes.pharmacy import app as app_pharmacy

from src.infra.configs import api

from fastapi import APIRouter


api.include_router(app_admin)
api.include_router(app_pharmacy)


if __name__ == "__main__":
    uvicorn.run(api, port=3435)
