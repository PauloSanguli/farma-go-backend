import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter

from src.infra.configs import api
from src.infra.http.routes.admin import (
    admin_routes_delete,
    admin_routes_get,
    admin_routes_post,
)
from src.infra.http.routes.pharmacy import pharmacy_routes_post, pharmacy_routes_get, pharmacy_routes_patch
from src.infra.http.routes.user import user_routes_get, user_routes_post

api.include_router(admin_routes_get)
api.include_router(admin_routes_post)
api.include_router(admin_routes_delete)

api.include_router(pharmacy_routes_post)
api.include_router(pharmacy_routes_get)
api.include_router(pharmacy_routes_patch)

api.include_router(user_routes_get)
api.include_router(user_routes_post)

if __name__ == "__main__":
    uvicorn.run(api, port=3435, reload=True)
