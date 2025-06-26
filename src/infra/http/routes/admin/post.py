from typing import Annotated, Optional

from fastapi import UploadFile
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.domain.schemas import AuthSchema, CoordenatesSchema, PharmacySchema
from src.infra.http.controllers import AdminController
from src.infra.http.middleware.authorizators import JWTPermissionsHandler
from src.infra.http.repositorys import AdminRepository
from src.infra.models import AddressPharmacy, Admin, Pharmacist, Pharmacy

app = APIRouter(prefix="/admin", tags=["Admin"])

@app.post("/pharmacy")
async def regist_pharmacy(
    admin_logged: Annotated[dict, Depends(JWTPermissionsHandler.get_admin_logged)],
    pharmacy: Pharmacy,
    address: CoordenatesSchema,
    pharmacist: Pharmacist,
    # files: list[UploadFile],
    # urls: list[str] = None
):
    response: dict[str, str] = AdminRepository.regist_pharmacy(
        pharmacy, address, pharmacist
    )
    # images_name: list[str] = [image.filename for image in files]
    # return JSONResponse(
    #     content={"detal": images_name}
    # )
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)


@app.post("/pharmacy/pharmacist")
async def regist_pharmacist_in_pharmacy(
    admin_logged: Annotated[dict, Depends(JWTPermissionsHandler.get_admin_logged)],
    pharmacist: Pharmacist,
):
    response: dict[str, str] = AdminRepository.regist_pharmacist_in_pharmacy(pharmacist)
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)


@app.post("/login")
def admin_login(admin: AuthSchema):
    token: str = AdminController.authenticate_admin(admin)
    return JSONResponse(content={"token": token}, status_code=status.HTTP_201_CREATED)


@app.post("/create")
def create_admin(admin: Admin):
    response: dict[str, str] = AdminRepository.create_admin(admin)
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)




##
@app.patch("/pharmacy")
def update_pharmacy(
    admin_logged: Annotated[dict, Depends(JWTPermissionsHandler.get_admin_logged)],
    pharmacy: PharmacySchema,
    id: str
):
    response = AdminRepository.update_pharmacy(pharmacy, id)
    return JSONResponse(
        content=response,
        status_code=200
    )

@app.patch("/pharmacist")
def update_pharmacist(
    admin_logged: Annotated[dict, Depends(JWTPermissionsHandler.get_admin_logged)],
    pharmacist: Pharmacist,
    id: str
):
    response = AdminRepository.update_pharmacist(pharmacist, id)
    return JSONResponse(
        content=response,
        status_code=200
    )

