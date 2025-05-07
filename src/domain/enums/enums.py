from enum import Enum


class MedicineCategory(str, Enum):
    ANTIBIOTIC = "antibiotic"
    ANALGESIC = "analgesic"
    VITAMIN = "vitamin"
    ANTIHISTAMINE = "antihistamine"
    OTHER = "other"


class EntityRole(str, Enum):
    ADMIN = "admin"
    PHARMACIST = "pharmacist"
    USER = "user"

class FieldsAddressLocationiqMapperEnum(str, Enum):
    street = "ROAD"
    neighborhood = "SUBURB"
    neighborhood = "TOWN"
    city = "COUNTY"
    state = "STATE"
