from fastapi import APIRouter

from src.infra.http.controllers import UserController

from typing import Annotated

from fastapi import Depends
from fastapi import status
from fastapi.responses import JSONResponse

from src.infra.http.middleware.authorizators import JWTPermissionsHandler
from src.domain.schemas import UserUpdateSchema

app = APIRouter(prefix="/user", tags=["User"])

@app.patch("/")
def update_profile_data(
    user_logged: Annotated[dict[str, str], Depends(JWTPermissionsHandler.get_user_logged)],
    user_data: UserUpdateSchema
):
    response: dict = UserController.update_user_partial(user_logged.get("id"), user_data.__dict__)
    return JSONResponse(
        content=response,
        status_code=status.HTTP_200_OK
    )
