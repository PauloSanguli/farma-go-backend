from enum import Enum



class MedicineCategory(str, Enum):
    ANTIBIOTIC = "antibiotic"
    ANALGESIC = "analgesic"
    VITAMIN = "vitamin"
    ANTIHISTAMINE = "antihistamine"
    OTHER = "other"


class UserRole(str, Enum):
    ADMIN = "admin"
    PHARMACIST = "pharmacist"
    USER = "user"
