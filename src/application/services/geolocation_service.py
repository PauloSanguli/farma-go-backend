import json
import requests
from os import getenv
from fastapi import status
from fastapi.exceptions import HTTPException


class GeolocationService:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

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

    def _retrieve_address(self, retries: int = 3, api_name: str = "nominatim", debug: bool = False) -> dict:
        url = self.__base_urls.get(api_name)
        if not url:
            raise ValueError(f"Unsupported API name '{api_name}'.")

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data: dict = response.json()
                if debug:
                    with open(f"examples/{api_name}.json", "w") as file:
                        file.write(json.dumps(data, indent=4))
                return data.get("address")
            else:
                raise requests.RequestException(f"Status code: {response.status_code}")
        except requests.RequestException as e:
            if retries > 0:
                return self._retrieve_address(retries - 1, api_name, debug)
            raise HTTPException(
                detail=f"Failed to get location from {api_name}: {e}",
                status_code=status.HTTP_400_BAD_REQUEST
            )
