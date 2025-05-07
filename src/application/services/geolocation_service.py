import json
import requests
from os import getenv
from fastapi import status
from fastapi.exceptions import HTTPException

from src.application.utils.mappers_util import retrieve_enum_mapper_for_api

from src.domain.enums import FieldsAddressLocationiqMapperEnum


class GeolocationService:
    def __init__(self, latitude: float, longitude: float, api_name: str = "locationiq"):
        self.latitude = latitude
        self.longitude = longitude
        self.api_name = api_name
        self.enum_fields = retrieve_enum_mapper_for_api(api_name)

        self.__base_urls: dict[str, str] = {
            "locationiq": (
                f"https://us1.locationiq.com/v1/reverse?key={getenv('GEOLOCATION_LOCATION_API_KEY')}"
                f"&lat={latitude}&lon={longitude}&format=json"
            ),
            "opencage": (
                f"https://api.opencagedata.com/geocode/v1/json"
                f"?q={latitude},{longitude}&key={getenv('GEOLOCATION_GEOCODING_API_KEY')}"
            ),
            "nominatim": f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
        }

    def _retrieve_address(self, retries: int = 3, debug: bool = False) -> dict:
        url = self.__base_urls.get(self.api_name)
        if not url:
            raise ValueError(f"Unsupported API name '{self.api_name}'.")

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data: dict = response.json()
                if debug:
                    with open(f"examples/{self.api_name}.json", "w") as file:
                        file.write(json.dumps(data, indent=4))
                address: dict = data.get("address")
                return {
                    "city": address.get(self.enum_fields.city),
                    "street": address.get(self.enum_fields.street),
                    "neighborhood": address.get(self.enum_fields.neighborhood),
                    "state": address.get(self.enum_fields.state)
                }
            else:
                raise requests.RequestException(f"Status code: {response.status_code}")
        except requests.RequestException as e:
            if retries > 0:
                return self._retrieve_address(retries - 1, self.api_name, debug)
            raise HTTPException(
                detail=f"Failed to get location from {self.api_name}: {e}",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def retrieve_location(retrys: int = 3, debug: bool = False) -> dict[str, float] | None:
        try:
            response = requests.get("https://ipinfo.io/json", timeout=10)
            if response.status_code == 200:
                data = response.json()
                location = data.get("loc", None)
                if location:    
                    latitude, longitude = map(float, location.split(","))
                    return {
                        "latitude": latitude,
                        "longitude": longitude
                    }
            raise HTTPException(
                detail="Error trying getting the location of pharmacy",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except requests.RequestException as e:
            if retrys > 0:
                return GeolocationService.retrieve_location(retrys - 1, debug)
        raise HTTPException(
            detail="Location dont getted for pharmacy",
            status_code=status.HTTP_400_BAD_REQUEST
        )
