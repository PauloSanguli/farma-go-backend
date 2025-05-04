from abc import ABC, abstractmethod
from typing import Dict

from src.infra.models import AddressPharmacy, Pharmacist, Pharmacy


class IAdminRepository(ABC):
    @abstractmethod
    def regist_pharmacy(
        self,
        pharmacy: Pharmacy,
        address: AddressPharmacy,
        pharmacist: Pharmacist,
    ) -> Dict[str, str]:
        NotImplementedError("Method 'regist_pharmacy' should be implemented!")

    @abstractmethod
    def delete_pharmacy(pharmacy_id: str) -> Pharmacy:
        NotImplementedError("Method 'delete_pharmacy' should be implemented!")

    @abstractmethod
    def list_pharmacys() -> list[Pharmacy]:
        NotImplementedError("Method 'list_pharmacys' should be implemented!")

    @abstractmethod
    def regist_pharmacist_in_pharmacy(
        pharmacy_id: str, pharmacist: Pharmacist
    ) -> dict[str, str]:
        NotImplementedError(
            "Method 'regist_pharmacist_in_pharmacy' should be implemented!"
        )
