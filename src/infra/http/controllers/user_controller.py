from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from src.domain.schemas import AuthSchema
from src.infra.configs import get_session
from src.infra.http.middleware.authenticators import JwtHandler
from src.infra.models import User, Medicine, Stock, Pharmacy, UserSearchHistory
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
    def search_medicine_in_pharmacy_stock(medicine_name: str, user_id: str) -> dict:
        session: Session = get_session()
        UserController.regist_history(medicine_name, user_id)
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

    @staticmethod
    def update_user_partial(user_id: str, data: dict) -> dict[str, str]:
        session = get_session()
        user = session.get(User, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {
            "detail": 'User data updated'
        }
    
    @staticmethod
    def regist_history(query: str, user_id: str) -> None:
        session: Session = get_session()
        history = UserSearchHistory(
            query=query,
            user_id=user_id
        )
        session.add(history)
        session.commit()
