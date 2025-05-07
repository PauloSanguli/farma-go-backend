from src.domain.schemas import AddressPharmacySchema
from src.application.services.geolocation_service import GeolocationService


def validate_location(address_schema: AddressPharmacySchema) -> AddressPharmacySchema:
        try:
            lat = float(address_schema.latitude)
            lon = float(address_schema.longitude)
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError
        except (TypeError, ValueError):
            location: dict[str, float] = GeolocationService.retrieve_location()

            address_schema.latitude = float(location.get("latitude"))
            address_schema.longitude = float(location.get("longitude"))
        return address_schema
