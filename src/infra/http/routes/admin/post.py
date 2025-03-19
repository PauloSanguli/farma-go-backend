from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

from src.infra.http.repositorys import AdminRepository

from src.infra.models import Pharmacy



app = APIRouter(prefix="/admin")

@app.post("/pharmacy")
async def regist_pharmacy(pharmacy: Pharmacy):
    return JSONResponse(
        content={},
        status_code=status.HTTP_201_CREATED
    )
