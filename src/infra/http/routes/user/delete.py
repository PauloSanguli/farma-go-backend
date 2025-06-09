from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.infra.http.controllers import UserController
from src.infra.http.middleware.authorizators import JWTPermissionsHandler

app = APIRouter(prefix="/user", tags=["User"])


@app.delete("/search-history/")
def clean_user_search_history(
    user_logged: Annotated[
        dict[str, str], Depends(JWTPermissionsHandler.get_user_logged)
    ]
):
    UserController.clean_history_search(user_logged.get("id"))
    return JSONResponse(content={
        "detail": "User history was already cleaned!"
    }, status_code=status.HTTP_200_OK)
