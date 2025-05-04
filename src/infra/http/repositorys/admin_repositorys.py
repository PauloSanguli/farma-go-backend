from typing import Type

from src.domain.schemas import PharmacySchema

from src.infra.models import Pharmacy, PharmacyImage, AddressPharmacy, Pharmacist, Stock

from sqlmodel import Session

from src.infra.configs import get_session

from src.application.repositorys import IAdminRepository


class AdminRepository(IAdminRepository):
    @staticmethod
    def regist_pharmacy(
        pharmacy: Pharmacy,
        address: AddressPharmacy,
        pharmacist: Pharmacist,
    ) -> dict[str, str]:
        session: Session = get_session()

        stock = Stock(pharmacy_id=pharmacy.id)

        pharmacy.address_id = address.id
        pharmacist.pharmacy_id = pharmacy.id
        pharmacy.stock_id = stock.id

        session.add_all([pharmacy, address, pharmacist, stock])
        session.commit()
        return {"detail": "Pharmacy created with successfuly"}
