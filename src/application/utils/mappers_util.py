from src.domain.enums import FieldsAddressLocationiqMapperEnum


def retrieve_enum_mapper_for_api(api_name: str) -> any:
    match api_name:
        case "locationiq":
            return FieldsAddressLocationiqMapperEnum
