from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from src.domain.schemas import AuthSchema
from src.infra.configs import get_session
from src.infra.http.middleware.authenticators import JwtHandler
from src.infra.models import Pharmacy, Pharmacist



class PharmacyController:
    def authenticate_pharmacist(pharmacist_schema: AuthSchema) -> str | Pharmacist:
        session: Session = get_session()
        jwt_handler = JwtHandler()

        query = select(Pharmacist).options(
            selectinload(Pharmacist.pharmacy)
        ).where(Pharmacist.email==pharmacist_schema.email)
        pharmacist = session.exec(query).first()
        pharmacist._check_password()
        # print(f"PHARMACIST: {pharmacist}")
        return pharmacist