from typing import Type
from src.infra.models import Medicine
from src.infra.configs import get_session

from sqlmodel import Session


class PharmacyRepository:
    @staticmethod
    def regist_medicine(medicine: Type[Medicine]):
        session: Type[Session] = get_session()
        session.add(medicine)
        session.commit()
