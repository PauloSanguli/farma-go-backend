from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from src.domain.schemas import AuthSchema
from src.infra.configs import get_session
from src.infra.http.middleware.authenticators import JwtHandler
from src.infra.models import Pharmacy, Pharmacist



class PharmacyController:
    def authenticate_pharmacist(pharmacist_data: AuthSchema) -> dict[str, str]:
        session: Session = get_session()
        jwt_handler = JwtHandler()

        query = select(Pharmacist).options(
            selectinload(Pharmacist.pharmacy)
        ).where(Pharmacist.email==pharmacist_data.email)
        pharmacist = session.exec(query).first()
        if not pharmacist:
            raise HTTPException(
                detail="Pharmacist not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        pharmacist._check_password(pharmacist_data.password)
        token: str = jwt_handler.create_token_pharmacist(pharmacist)
        return {
            "token": token
        }
