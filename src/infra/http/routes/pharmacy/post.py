from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.infra.http.repositorys import PharmacyRepository
from src.infra.http.controllers import PharmacyController
from src.infra.models import Medicine

from src.domain.schemas import AuthSchema, PharmacistSchema

app = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])


@app.post("/medicine")
def regist_medicine(medicine: Medicine):
    response: dict[str, str] = PharmacyRepository.regist_medicine(medicine)
    return JSONResponse(
        content=response,
        status_code=status.HTTP_201_CREATED,
    )

@app.post("/pharmacist/login", response_model=PharmacistSchema)
def pharmacist_login(pharmacist: AuthSchema):
    p = PharmacyController.authenticate_pharmacist(pharmacist)
    return p
