from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from src.domain.schemas import AdminSchema
from src.infra.configs import get_session
from src.infra.http.middleware.authenticators import JwtHandler
from src.infra.models import Admin


class AdminController:
    @staticmethod
    def authenticate_admin(admin_data: AdminSchema) -> str:
        session: Session = get_session()
        jwt_handler = JwtHandler()
        query = select(Admin).where(Admin.email == admin_data.email)
        admin = session.exec(query).first()
        if not admin:
            raise HTTPException(
                detail="Invalid email provided",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        admin._check_password(admin_data.password)
        return jwt_handler.create_token_admin(admin.id)
