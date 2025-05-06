from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from src.domain.schemas import AuthSchema
from src.infra.configs import get_session
from src.infra.http.middleware.authenticators import JwtHandler
from src.infra.models import User, Medicine, Stock, Pharmacy
from src.infra.http.repositorys import PharmacyRepository


class UserController:
    @staticmethod
    def authenticate_user(user_data: AuthSchema) -> str:
        session: Session = get_session()
        jwt_handler = JwtHandler()
        query = select(User).where(User.email == user_data.email)
        user = session.exec(query).first()
        if not user:
            raise HTTPException(
                detail="User not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        user._check_password(user_data.password)
        return jwt_handler.create_token_user(user.id)
    
    @staticmethod
    def search_medicine_in_pharmacy_stock(medicine_name: str) -> dict:
        session: Session = get_session()
        query = (
            select(Pharmacy)
            .join(Stock, Pharmacy.stock_id == Stock.id)
            .join(Medicine, Medicine.stock_id == Stock.id)
            .where(Medicine.name.ilike(f"%{medicine_name}%"))
        )
        result = session.exec(query).all()
        if len(result) == 0:
            raise HTTPException(
                status_code=404,
                detail="Medicine not found"
            )
        return result
