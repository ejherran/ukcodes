from typing import Any
import aioredis

class RedisClient:

    def __init__(self, url) -> None:
        self.redis = aioredis.from_url(url)
    
    async def get(self, key: str) -> str:
        return await self.redis.get(key)
    
    async def set(self, key: str, value: str) -> None:
        await self.redis.set(key, value)
    
    async def close(self) -> None:
        await self.redis.close()
        
    async def set_pool(self, keys: list, default: Any) -> None:
        for key in keys:
            await self.set(key, default)
