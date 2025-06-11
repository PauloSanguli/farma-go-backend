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
    Medicine
)

from src.application.services.geolocation_service import GeolocationService

from src.domain.validators.validators import validate_location


class AdminRepository(IAdminRepository):
    @staticmethod
    def export_data():
        session: Session = get_session()
        data = {}
        # Pega todos os dados das tabelas
        pharmacies = session.exec(select(Pharmacy)).all()
        pharmacists = session.exec(select(Pharmacist)).all()
        addresses = session.exec(select(AddressPharmacy)).all()
        images = session.exec(select(PharmacyImage)).all()
        stocks = session.exec(select(Stock)).all()
        medicines = session.exec(select(Medicine)).all()

        # Serializa os dados (convertendo para dicionários)
        data["pharmacies"] = [pharmacy.dict() for pharmacy in pharmacies]
        data["pharmacists"] = [pharmacist.dict() for pharmacist in pharmacists]
        data["addresses"] = [addr.dict() for addr in addresses]
        data["images"] = [img.dict() for img in images]
        data["stocks"] = [stock.dict() for stock in stocks]
        data["medicines"] = [med.dict() for med in medicines]
        return data

    @staticmethod
    def update_pharmacist(pharmacist: Pharmacist, id: str) -> dict:
        session: Session = get_session()

        # Busca o farmacêutico original
        db_pharmacist = session.exec(
            select(Pharmacist).where(Pharmacist.id == id)
        ).first()

        if not db_pharmacist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pharmacist '{pharmacist.id}' not found!"
            )

        # Atualiza os campos
        for key, value in pharmacist.dict(exclude_unset=True).items():
            if key != "id":
                setattr(db_pharmacist, key, value)

        session.commit()
        session.refresh(db_pharmacist)

        return {"detail": "Pharmacist was successfully updated!"}

    @staticmethod
    def update_pharmacy(data: PharmacySchema, id):
        session: Session = get_session()

        # Busca a farmácia no banco de dados
        pharmacy = session.exec(select(Pharmacy).where(Pharmacy.id == id)).first()
        if not pharmacy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pharmacy '{data.id}' not found!"
            )

        # Atualiza os dados da farmácia
        for key, value in data.dict(exclude={"address"}).items():
            if key != "id":
                setattr(pharmacy, key, value)

        # Atualiza o endereço, se fornecido
        if data.address:
            address = session.exec(select(AddressPharmacy).where(AddressPharmacy.id == pharmacy.address_id)).first()
            if address:
                for key, value in data.address.dict().items():
                    setattr(address, key, value)

        session.commit()
        session.refresh(pharmacy)  # opcional

        return {"detail": "Pharmacy updated successfully!"}


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
    def retrieve_pharmacist(id):
        session: Session = get_session()
        pharmacist = session.exec(
            select(Pharmacist).where(Pharmacist.id==id)
        ).first()
        session.close()
        return pharmacist
    
    @staticmethod
    def list_pharmacists() -> list:
        session: Session = get_session()
        pharmacists = session.exec(
            select(Pharmacist)
        ).all()
        session.close()
        return pharmacists

    @staticmethod
    def delete_pharmacy(pharmacy_id: str) -> dict[str, str]:
        session: Session = get_session()
        pharmacy = session.exec(
            select(Pharmacy).where(Pharmacy.id == pharmacy_id)
        ).first()

        if not pharmacy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pharmacy '{pharmacy_id}' not found!"
            )

        # Delete pharmacists
        for pharmacist in pharmacy.pharmacists:
            session.delete(pharmacist)

        # Delete pharmacy images
        for image in pharmacy.pharmacy_images:
            session.delete(image)

        # Delete stock + medicines
        if pharmacy.stock:
            for medicine in pharmacy.stock.medicines:
                session.delete(medicine)
            session.delete(pharmacy.stock)

        # Delete address (se quiser manter o endereço, comente esta parte)
        if pharmacy.address:
            session.delete(pharmacy.address)

        # Delete the pharmacy
        session.delete(pharmacy)
        session.commit()

        return {"detail": "Pharmacy was successfully deleted!"}
    
    @staticmethod
    def delete_pharmacist(pharmacist_id: str) -> dict[str, str]:
        session: Session = get_session()

        pharmacist = session.exec(
            select(Pharmacist).where(Pharmacist.id == pharmacist_id)
        ).first()

        if not pharmacist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pharmacist '{pharmacist_id}' not found!"
            )

        session.delete(pharmacist)
        session.commit()

        return {"detail": "Pharmacist was successfully deleted!"}


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
