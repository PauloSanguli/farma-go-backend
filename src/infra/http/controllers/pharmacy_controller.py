from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from src.domain.schemas import AuthSchema, MedicinestockSchema
from src.infra.configs import get_session
from src.infra.http.middleware.authenticators import JwtHandler
from src.infra.http.repositorys import PharmacyRepository
from src.infra.models import Medicine, Pharmacist, Pharmacy, Stock


class PharmacyController:
    def authenticate_pharmacist(pharmacist_data: AuthSchema) -> dict[str, str]:
        session: Session = get_session()
        jwt_handler = JwtHandler()

        query = (
            select(Pharmacist)
            .options(selectinload(Pharmacist.pharmacy))
            .where(Pharmacist.email == pharmacist_data.email)
        )
        pharmacist = session.exec(query).first()
        if not pharmacist:
            raise HTTPException(
                detail="Pharmacist not found", status_code=status.HTTP_404_NOT_FOUND
            )
        pharmacist._check_password(pharmacist_data.password)
        token: str = jwt_handler.create_token_pharmacist(pharmacist)
        return {"token": token}

    def update_medicine_stock(
        medicine_data: MedicinestockSchema, pharmacy_id: str
    ) -> dict:
        session: Session = get_session()

        result: dict = PharmacyRepository.retrieve_pharmacy_by_id(pharmacy_id)
        stock: Stock = result.get("stock")

        if not stock:
            raise HTTPException(
                detail="Stock not found!", status_code=status.HTTP_404_NOT_FOUND
            )

        medicine = session.exec(
            select(Medicine).where(Medicine.stock_id == stock.id)
        ).first()

        if not medicine:
            raise HTTPException(
                detail="Medicine not found!", status_code=status.HTTP_404_NOT_FOUND
            )

        medicine.quantity = medicine_data.quantity
        session.commit()
        session.refresh(medicine)

        return {
            "message": "Medicine stock updated successfully",
            "medicine_id": medicine.id,
        }

    def search_medicine_in_pharmacy_stock(pharmacy_id: str, medicine_name: str) -> dict:
        session: Session = get_session()
        stock: Stock = PharmacyRepository.retrieve_stock_pharmacy(pharmacy_id)

        query = select(Medicine).where(
            Medicine.name.ilike(f"%{medicine_name}%"), Medicine.stock_id == stock.id
        )
        result = session.exec(query).all()

        if not result:
            raise HTTPException(status_code=404, detail="Medicine not found")

        return result
