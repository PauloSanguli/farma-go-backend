from typing import Type

from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from src.domain.schemas import PharmacySchema
from src.infra.configs import get_session
from src.infra.models import AddressPharmacy, Medicine, Pharmacy, Stock


class PharmacyRepository:
    @staticmethod
    def regist_medicine(medicine: Medicine, pharmacy_id: str) -> dict[str, str]:
        session: Session = get_session()
        result: dict = PharmacyRepository.retrieve_pharmacy_by_id(pharmacy_id)
        stock: Stock = result.get("stock")
        medicine.stock_id = stock.id
        query = select(Medicine).where(
            Medicine.name.ilike(f"%{medicine.name}%"), Medicine.stock_id == stock.id
        )
        medicine_exists = session.exec(query).all()
        if len(medicine_exists) > 0:
            return {"detail": "This medicine already stay on that stock"}
        session.add(medicine)
        session.commit()
        session.close()
        return {"detail": "The medicine was already added to stock"}

    @staticmethod
    def retrieve_pharmacy_by_id(pharmacy_id: str) -> dict:
        session: Session = get_session()
        query = select(Pharmacy, Stock, AddressPharmacy).where(
            Pharmacy.stock_id == Stock.id, Pharmacy.id == pharmacy_id, Pharmacy.address_id==AddressPharmacy.id
        )
        result = session.exec(query).first()
        response = {"pharmacy": result[0], "stock": result[1], "address": result[2], "medicines": result[1].medicines} if result else None
        session.close()
        if not response:
            raise HTTPException(status_code=404, detail="Pharmacy not found")
        return response
