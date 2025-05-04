from typing import Type

from sqlmodel import Session

from src.infra.configs import get_session
from src.infra.models import Medicine


class PharmacyRepository:
    @staticmethod
    def regist_medicine(medicine: Type[Medicine]):
        # add that medicine on the real stock

        session: Session = get_session()
        session.add(medicine)
        session.commit()
        return {"detail": "The medicine was already added to stock"}
