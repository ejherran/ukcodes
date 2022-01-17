from operator import le
import os
import sys
import asyncio
import aio_pika
import json

from rabbit_consumer import RabbitConsumer
from post_codes_client import PostCodesClient
from post_codes_processor import PostCodesProcessor
from redis_client import RedisClient

from tasks import save_to_db

from db import Db
from db import Base

db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', '13306')
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', 'QweZxc123')
db_name = os.environ.get('DB_NAME', 'ukcodes')
db_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

rabbit_host = os.environ.get('RABBIT_HOST', 'localhost')
rabbit_port = os.environ.get('RABBIT_PORT', '5672')
rabbit_user = os.environ.get('RABBIT_USER', 'rabbit')
rabbit_password = os.environ.get('RABBIT_PASSWORD', 'QweZxc123')
rabbit_vhost = os.environ.get('RABBIT_VHOST', 'my_vhost')
rabbit_queue = os.environ.get('RABBIT_QUEUE', 'coordinates_to_process')
rabbit_url = f'amqp://{rabbit_user}:{rabbit_password}@{rabbit_host}:{rabbit_port}/{rabbit_vhost}'

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', '6379')
redis_password = os.environ.get('REDIS_PASSWORD',  'QweZxc123')
redis_db = os.environ.get('REDIS_DB', '0')
redis_url = f'redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}'

async def process_message(message: bytes) -> None:
    
    redis = RedisClient(redis_url)

    coordinates = json.loads(message.decode('utf-8'))
    count_coordinates = len(coordinates)

    post_codes = await PostCodesClient(coordinates, redis).get_postcodes()
    count_consult_codes = len(post_codes)

    post_codes = PostCodesProcessor(post_codes).process_post_codes()
    count_valid_codes = len(post_codes)

    save_to_db.delay(post_codes)

    print(f'{count_coordinates} coordinates received - {count_consult_codes} consulted postcodes - {count_valid_codes} new and valid postcodes')

async def main(loop: asyncio.AbstractEventLoop) -> aio_pika.connection.Connection:
    
    db = Db(db_url)
    db.create_schema(Base)
    coordinates = db.get_coordinates()

    redis = RedisClient(redis_url)
    await redis.set_pool(coordinates, b'1')
    await redis.close()

    rabbit_client = RabbitConsumer(loop, rabbit_url, rabbit_queue, process_message)
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