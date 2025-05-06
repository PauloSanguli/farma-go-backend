from typing import Type

from sqlmodel import Session, select

from fastapi.exceptions import HTTPException

from src.infra.configs import get_session
from src.infra.models import Medicine, Stock, Pharmacy, AddressPharmacy
from src.domain.schemas import PharmacySchema


class PharmacyRepository:
    @staticmethod
    def regist_medicine(medicine: Medicine, pharmacy_id: str) -> dict[str, str]:
        # add that medicine on the real stock
        session: Session = get_session()
        stock: Stock = PharmacyRepository.retrieve_stock_pharmacy(pharmacy_id)
        medicine.stock_id = stock.id
        session.add(medicine)
        session.commit()
        return {"detail": "The medicine was already added to stock"}
    
    @staticmethod
    def retrieve_stock_pharmacy(pharmacy_id: str) -> Stock:
        session: Session = get_session()
        result: dict = PharmacyRepository.retrieve_pharmacy_by_id(pharmacy_id)
        return result.get("stock")
    
    @staticmethod
    def retrieve_pharmacy_by_id(pharmacy_id: str) -> dict:
        session: Session = get_session()
        query = select(Pharmacy, Stock, AddressPharmacy).where(
            Pharmacy.stock_id == Stock.id,
            Pharmacy.id == pharmacy_id
        )
        result = session.exec(query).first()
        if not result:
            raise HTTPException(status_code=404, detail="Pharmacy not found")
        return {
            "pharmacy": result[0],
            "stock": result[1],
            "address": result[2]
        }


