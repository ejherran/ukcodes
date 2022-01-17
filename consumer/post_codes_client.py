import requests

class PostCodesClient:

    def __init__(self, coordinates: list) -> None:
        self.coordinates = coordinates
        self.url = 'https://api.postcodes.io/postcodes'
    
    def get_postcodes(self) -> list:
        
        postcodes = []
        
        payload = {"geolocations":[]}
        
        for coordinate in self.coordinates:
            parts = coordinate.split(',')
            payload["geolocations"].append({"latitude": parts[0], "longitude": parts[1], "limit": 1})
        
        response = requests.post(self.url, json=payload, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            return response.json()['result']
        else:
            return []