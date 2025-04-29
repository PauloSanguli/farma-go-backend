from src.infra.models import Medicine
from src.infra.http.repositorys import PharmacyRepository

from fastapi import status
from fastapi import APIRouter

from fastapi.responses import JSONResponse


app = APIRouter(prefix="/pharmacy")


@app.post("/medicine")
def regist_medicine(medicine: Medicine):
    PharmacyRepository.regist_medicine(medicine)
    return JSONResponse(
        content={"detail": "The medicine was already added to stock"},
        status_code=status.HTTP_201_CREATED,
    )
