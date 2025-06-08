import requests

def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data.get("loc", "")  # retorna algo como "latitude,longitude"
        if loc:
            latitude, longitude = map(float, loc.split(","))
            return latitude, longitude
        else:
            return None, None
    except Exception as e:
        print("Erro ao obter localização:", e)
        return None, None

lat, lon = get_location()
print(f"Latitude: {lat}, Longitude: {lon}")
