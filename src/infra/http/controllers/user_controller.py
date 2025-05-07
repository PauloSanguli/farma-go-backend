from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from sqlalchemy import and_

from src.domain.schemas import AuthSchema

from src.infra.configs import get_session
from src.infra.http.middleware.authenticators import JwtHandler
from src.infra.http.repositorys import PharmacyRepository
from src.infra.models import Medicine, Pharmacy, Stock, User, UserSearchHistory, AddressPharmacy

from src.application.utils.mappers_util import retrieve_enum_mapper_for_api

from src.application.services.geolocation_service import GeolocationService


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
    def search_medicine_in_pharmacy_stock(medicine_name: str, latitude: float, longitude: float, user_id: str) -> dict:
        session: Session = get_session()
        geolocation_service = GeolocationService(
            latitude=latitude,
            longitude=longitude,
            api_name="locationiq"
        )
        address_details: dict = geolocation_service._retrieve_address()

        UserController.regist_history(medicine_name, user_id)
        query = (
            select(Pharmacy)
            .join(AddressPharmacy, Pharmacy.address_id == AddressPharmacy.id)
            .join(Stock, Pharmacy.stock_id == Stock.id)
            .join(Medicine, Medicine.stock_id == Stock.id)
            .where(
                and_(
                    Pharmacy.opened==True,
                    Medicine.name.ilike(f"%{medicine_name}%"),
                    Medicine.quantity>0,
                    AddressPharmacy.city.ilike(f"%{address_details.get('city')}%"),
                    AddressPharmacy.neighborhood.ilike(f"%{address_details.get('neighborhood')}%"),
                    AddressPharmacy.state.ilike(f"%{address_details.get('state')}%"),
                    AddressPharmacy.street.ilike(f"%{address_details.get('street')}%")
                )
            )
        )
        result = session.exec(query).all()
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Medicine not found")
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
        return {"detail": "User data updated"}

    @staticmethod
    def regist_history(query: str, user_id: str) -> None:
        session: Session = get_session()
        history = UserSearchHistory(query=query, user_id=user_id)
        session.add(history)
        session.commit()
