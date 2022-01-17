import os
from celery import Celery
from file_analyzer import FileAnalizer

# rabbit_host = os.environ.get('RABBIT_HOST', 'localhost')
# rabbit_port = os.environ.get('RABBIT_PORT', '5672')
# rabbit_user = os.environ.get('RABBIT_USER', 'guest')
# rabbit_password = os.environ.get('RABBIT_PASSWORD', 'guest')
# rabbit_vhost = os.environ.get('RABBIT_VHOST', 'my_vhost')
# rabbit_queue = os.environ.get('RABBIT_QUEUE', 'coordinates_to_process')
# rabbit_url = f'amqp://{rabbit_user}:{rabbit_password}@{rabbit_host}:{rabbit_port}/{rabbit_vhost}'
app = Celery('tasks', broker="redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@localhost:6379/0", backend="rpc://")

@app.task
def analyze_file(data: str) -> dict:
    
    file_analyzer = FileAnalizer(data)
    coordinates, warnings = file_analyzer.analyze()

    return warnings