import asyncio
import aio_pika
import json

class RabbitPublisher:

    def __init__(self, url: str, queue_name: str) -> None:
        
        self.url = url
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
    
    async def connect(self) -> None:

        self.connection = await aio_pika.connect_robust(self.url)
    
    async def send(self, coordinates: list) -> None:
        
        async with self.connection:
            self.channel = await self.connection.channel()
            
            await self.channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(coordinates).encode()),
            routing_key=self.queue_name,
        )