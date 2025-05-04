from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import Session, delete, select

from src.application.repositorys import IAdminRepository
from src.domain.schemas import PharmacySchema
from src.infra.configs import get_session
from src.infra.models import AddressPharmacy, Pharmacist, Pharmacy, PharmacyImage, Stock


class AdminRepository(IAdminRepository):
    @staticmethod
    def regist_pharmacy(
        pharmacy: Pharmacy,
        address: AddressPharmacy,
        pharmacist: Pharmacist,
    ) -> dict[str, str]:
        try:
            session: Session = get_session()

            stock = Stock(pharmacy_id=pharmacy.id)

            pharmacy.address_id = address.id
            pharmacist.pharmacy_id = pharmacy.id
            pharmacy.stock_id = stock.id

            session.add_all([pharmacy, address, pharmacist, stock])
        except IntegrityError:
            raise HTTPException(
                detail="Error during creation of pharmacy",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        session.commit()
        return {"detail": "Pharmacy created with successfuly"}

    @staticmethod
    def list_pharmacys():
        session: Session = get_session()
        statement = select(Pharmacy).options(selectinload(Pharmacy.address))
        pharmacys = session.exec(statement).all()
        return pharmacys

    @staticmethod
    def delete_pharmacy(pharmacy_id: str):
        session: Session = get_session()
        pharmacy = session.exec(select(Pharmacy).where(Pharmacy.id == pharmacy_id)).first()
        if not pharmacy:
            raise HTTPException(
                detail=f"Pharmacy '{pharmacy_id}' don't finded!",
                status_code=status.HTTP_404_NOT_FOUND
            )
        session.delete(pharmacy)
        return {"detail": "Pharmacy was sucessfuly deleted!"}
