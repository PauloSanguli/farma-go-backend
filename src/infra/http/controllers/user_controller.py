from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select, delete
from sqlalchemy import and_

from src.domain.schemas import AuthSchema

from src.infra.configs import get_session
from src.infra.http.middleware.authenticators import JwtHandler
from src.infra.http.repositorys import PharmacyRepository
from src.infra.models import Medicine, Pharmacy, Stock, User, UserSearchHistory, AddressPharmacy, PharmacyImage

from src.application.utils.mappers_util import retrieve_enum_mapper_for_api

from src.application.services.geolocation_service import GeolocationService

class UserController:
    @staticmethod
    def authenticate_user(user_data: AuthSchema) -> str:
        jwt_handler = JwtHandler()
        with get_session() as session:
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
    def search_medicine_in_pharmacy_stock(
        medicine_name: str,
        latitude: float,
        longitude: float,
        user_id: str,
        price: float | None,
        category: str | None,
        avaliation: int | None,
        nearby_pharmacys: bool
    ) -> list:
        geolocation_service = GeolocationService(
            latitude=latitude,
            longitude=longitude,
            api_name="locationiq"
        )
        address_details: dict = geolocation_service._retrieve_address()

        if medicine_name or category:
            UserController.regist_history(medicine_name or f"{category}, {price}", user_id)

        with get_session() as session:
            filters = [
                Pharmacy.opened == True,
                Medicine.quantity > 0,
            ]
            if medicine_name is not None and medicine_name.strip() != "":
                filters.append(Medicine.name.ilike(f"%{medicine_name}%"))

            if nearby_pharmacys:
                filters.extend([
                    AddressPharmacy.city.ilike(f"%{address_details.get('city')}%"),
                    AddressPharmacy.neighborhood.ilike(f"%{address_details.get('neighborhood')}%"),
                    AddressPharmacy.state.ilike(f"%{address_details.get('state')}%"),
                ])

            if price is not None:
                filters.append(Medicine.price <= price)

            if category is not None and category.strip() != "":
                filters.append(Medicine.category == category.upper())


            # if avaliation is not None:
            #     filters.append(Pharmacy.avaliation >= avaliation)

            query = (
                select(Pharmacy)
                .join(AddressPharmacy, Pharmacy.address_id == AddressPharmacy.id)
                .join(Stock, Pharmacy.stock_id == Stock.id)
                .join(Medicine, Medicine.stock_id == Stock.id)
                .where(and_(*filters))
            )

            result = session.exec(query).all()

            # Ordena pelas farmácias mais próximas, se solicitado
            # if nearby_pharmacys:
            #     result.sort(key=lambda pharmacy: GeolocationService.calculate_distance(
            #         latitude, longitude,
            #         pharmacy.address.latitude,
            #         pharmacy.address.longitude
            #     ))

            if not result:
                raise HTTPException(status_code=404, detail="Medicine not found")

            return result


    @staticmethod
    def update_user_partial(user_id: str, data: dict) -> dict[str, str]:
        with get_session() as session:
            user = session.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            for key, value in data.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)

            session.add(user)
            session.commit()
            session.refresh(user)
            session.close()
            return {"detail": "User data updated"}

    @staticmethod
    def regist_history(query: str, user_id: str) -> None:
        with get_session() as session:
            history = UserSearchHistory(query=query, user_id=user_id)
            session.add(history)
            session.commit()
            session.close()

    @staticmethod
    def clean_history_search(user_id: str) -> None:
        session: Session = get_session()
        query = delete(UserSearchHistory).where(UserSearchHistory.user_id==user_id)
        session.exec(query)
        session.commit()
        session.close()
    