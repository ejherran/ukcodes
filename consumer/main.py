from operator import le
import os
import sys
import asyncio
import aio_pika
import json

from rabbit_consumer import RabbitConsumer
from post_codes_client import PostCodesClient
from post_codes_processor import PostCodesProcessor

async def process_message(message: bytes) -> None:
    
    coordinates = json.loads(message.decode('utf-8'))
    print(len(coordinates))
    # post_codes = PostCodesClient(coordinates).get_postcodes()
    # post_codes = PostCodesProcessor(post_codes).process_post_codes()

    # print(len(post_codes))

async def main(loop: asyncio.AbstractEventLoop) -> aio_pika.connection.Connection:
    
    rabbit_host = os.environ.get('RABBIT_HOST', 'localhost')
    rabbit_port = os.environ.get('RABBIT_PORT', '5672')
    rabbit_user = os.environ.get('RABBIT_USER', 'guest')
    rabbit_password = os.environ.get('RABBIT_PASSWORD', 'guest')
    rabbit_queue = os.environ.get('RABBIT_QUEUE', 'coordinates_to_process')
    rabbit_client = RabbitConsumer(loop, f'amqp://{rabbit_user}:{rabbit_password}@{rabbit_host}:{rabbit_port}/my_vhost', rabbit_queue, process_message)
    connection = await rabbit_client.connect()

    return connection


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    connection = loop.run_until_complete(main(loop))

    if connection is None:
        
        sys.exit("Failure to connect to RabbitMQ...\n") 
        
    else:
        print('Connected to RabbitMQ: Ready to process messages...\n')
        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(connection.close())