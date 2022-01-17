import asyncio
import os
from celery import Celery
from file_analyzer import FileAnalizer
from rabbit_publisher import RabbitPublisher

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

app = Celery('tasks', broker=redis_url, backend="rpc://")

@app.task
def analyze_file(data: str) -> dict:
    
    file_analyzer = FileAnalizer(data)
    coordinates, warnings = file_analyzer.analyze()

    send_coordinates.delay(coordinates)

    return warnings

@app.task
def send_coordinates(coordinates: list) -> str:
    
    count = 0

    while len(coordinates) > 0:
        count += 1

        if len(coordinates) >= 100:
            asyncio.run(put_to_queue(coordinates[:100]))
            coordinates = coordinates[100:]
        else:
            asyncio.run(put_to_queue(coordinates))
            break

    return f'{count} coordinates packages sent to "{rabbit_queue}" queue.'

async def put_to_queue(coordinates: list) -> None:

    publisher = RabbitPublisher(rabbit_url, rabbit_queue)
    await publisher.connect()
    await publisher.send(coordinates)

