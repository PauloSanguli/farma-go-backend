from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import Session, delete, select

from src.application.repositorys import IAdminRepository
from src.domain.schemas import PharmacySchema, CoordenatesSchema
from src.infra.configs import get_session
from src.infra.models import (
    AddressPharmacy,
    Admin,
    Pharmacist,
    Pharmacy,
    PharmacyImage,
    Stock,
)

from src.application.services.geolocation_service import GeolocationService

from src.domain.validators.validators import validate_location


class AdminRepository(IAdminRepository):
    @staticmethod
    def regist_pharmacy(
        pharmacy: Pharmacy,
        address_data: CoordenatesSchema,
        pharmacist: Pharmacist,
    ) -> dict[str, str]:
        try:
            address: AddressPharmacy = AdminRepository.create_address_pharmacy(address_data)
            session: Session = get_session()

            stock = Stock(pharmacy_id=pharmacy.id)

            pharmacy.address_id = address.id
            pharmacist.pharmacy_id = pharmacy.id
            pharmacy.stock_id = stock.id
            pharmacist._encrypt_password()

            session.add_all([pharmacy, address, pharmacist, stock])
        except IntegrityError as e:
            raise HTTPException(
                detail=f"Error during creation of pharmacy: {e._message()}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        session.commit()
        session.close()
        return {"detail": "Pharmacy created with successfuly"}

    @staticmethod
    def list_pharmacys() -> list[Pharmacy]:
        session: Session = get_session()
        statement = select(Pharmacy).options(selectinload(Pharmacy.address))
        pharmacys = session.exec(statement).all()
        session.close()
        return pharmacys

    @staticmethod
    def delete_pharmacy(pharmacy_id: str) -> dict[str, str]:
        session: Session = get_session()
        pharmacy = session.exec(
            select(Pharmacy).where(Pharmacy.id == pharmacy_id)
        ).first()
        if not pharmacy:
            raise HTTPException(
                detail=f"Pharmacy '{pharmacy_id}' don't finded!",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        session.delete(pharmacy)
        session.close()
        return {"detail": "Pharmacy was sucessfuly deleted!"}

    @staticmethod
    def regist_pharmacist_in_pharmacy(pharmacist: Pharmacist) -> dict[str, str]:
        session: Session = get_session()
        try:
            pharmacy = session.exec(
                select(Pharmacy).where(Pharmacy.id == pharmacist.pharmacy_id)
            ).first()
            if not pharmacy:
                raise HTTPException(
                    detail=f"Pharmacy '{pharmacist.pharmacy_id}' don't finded!",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            pharmacist._encrypt_password()
            session.add(pharmacist)
            session.commit()
        except IntegrityError as e:
            raise HTTPException(
                detail=f"An error occured: {e._message()}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        session.close()
        return {"detail": "Pharmacist was sucessufuly created!"}

    @staticmethod
    def create_admin(admin: Admin) -> dict[str, str]:
        session: Session = get_session()
        admin._encrypt_password()
        session.add(admin)
        session.commit()
        session.close()
        return {"detail": "admin was created with successfuly!"}

    @staticmethod
    def create_address_pharmacy(address_data: CoordenatesSchema) -> AddressPharmacy:
        address_data = validate_location(address_data)

        geolocation_service = GeolocationService(
            latitude=address_data.latitude,
            longitude=address_data.longitude
        )
        address_details: dict = geolocation_service._retrieve_address()
        address = AddressPharmacy(
            city=address_details.get("city"),
            neighborhood=address_details.get("neighborhood"),
            street=address_details.get("street"),
            state=address_details.get("state"),
            zip_code=address_data.zip_code,
            latitude=address_data.latitude,
            longitude=address_data.longitude
        )
        return address
