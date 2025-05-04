from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.infra.http.repositorys import PharmacyRepository
from src.infra.models import Medicine

app = APIRouter(prefix="/pharmacy")


@app.post("/medicine")
def regist_medicine(medicine: Medicine):
    PharmacyRepository.regist_medicine(medicine)
    return JSONResponse(
        content={"detail": "The medicine was already added to stock"},
        status_code=status.HTTP_201_CREATED,
    )
