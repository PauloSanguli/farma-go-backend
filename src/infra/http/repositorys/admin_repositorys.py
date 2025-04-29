from typing import Type

from src.domain.schemas import PharmacySchema

from src.infra.models import Pharmacy, PharmacyImage, AddressPharmacy, Pharmacist

from sqlmodel import Session

from src.infra.configs import get_session


class AdminRepository:
    @staticmethod
    def regist_pharmacy(
        pharmacy: Type[PharmacySchema],
        address: Type[AddressPharmacy],
        pharmacist: Type[Pharmacist],
    ) -> Type[any]:
        session: Type[Session] = get_session()
        pharmacy.address_id = address.id
        pharmacist.pharmacy_id = pharmacy.id
        session.add_all([pharmacy, address, pharmacist])
        session.commit()
        return {"detail": "Pharmacy created with successfuly"}
