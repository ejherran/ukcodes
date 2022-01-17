import requests

from redis_client import RedisClient

class PostCodesClient:

    def __init__(self, coordinates: list, cache: RedisClient) -> None:
        self.coordinates = coordinates
        self.cache = cache
        self.url = 'https://api.postcodes.io/postcodes'
    
    async def get_postcodes(self) -> list:
        
        postcodes = []
        
        payload = {"geolocations":[]}
        
        for coordinate in self.coordinates:

            if(await self.cache.get(coordinate) is None):
                await self.cache.set(coordinate, b'1')
                parts = coordinate.split(',')
                payload["geolocations"].append({"latitude": parts[0], "longitude": parts[1], "limit": 1})
        
        response = requests.post(self.url, json=payload, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            return response.json()['result']
        else:
            return []