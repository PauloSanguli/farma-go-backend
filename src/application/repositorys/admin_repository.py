from abc import ABC, abstractmethod
from src.infra.models import Pharmacy, AddressPharmacy, Pharmacist
from typing import Dict


class IAdminRepository(ABC):
    @abstractmethod
    def regist_pharmacy(
        self,
        pharmacy: Pharmacy,
        address: AddressPharmacy,
        pharmacist: Pharmacist,
    ) -> Dict[str, str]:
        NotImplementedError("Method 'regist_pharmacy' should be implemented!")
