from asyncio import AbstractEventLoop
from typing import Callable, Coroutine, Any
from aio_pika import IncomingMessage
from aio_pika.connection import Connection
import aio_pika

class RabbitConsumer:
    
    def __init__(self, loop: AbstractEventLoop, url: str, queue_name: str, callback: Callable[..., Coroutine], prefetch_count: int = 1000) -> None:
        
        self.loop = loop
        self.url = url
        self.queue_name = queue_name
        self.callback = callback
        self.prefetch_count = prefetch_count
        self.connection = None
        self.channel = None
        self.queue = None
    
    async def connect(self) -> Connection:
        
        try:
            self.connection = await aio_pika.connect_robust(self.url, loop=self.loop)

            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=self.prefetch_count)

            self.queue = await self.channel.declare_queue(self.queue_name, auto_delete=True)
            await self.queue.consume(self.__process_message)

            return self.connection

        except Exception as e:
            return None

    async def __process_message(self, message: IncomingMessage):
            
        async with message.process():
            await self.callback(message.body)
