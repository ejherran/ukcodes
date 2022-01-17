import os
from re import I
from celery import Celery

from db import Coordinate, Db
from db import Base

rabbit_host = os.environ.get('RABBIT_HOST', 'localhost')
rabbit_port = os.environ.get('RABBIT_PORT', '5672')
rabbit_user = os.environ.get('RABBIT_USER', 'rabbit')
rabbit_password = os.environ.get('RABBIT_PASSWORD', 'QweZxc123')
rabbit_vhost = os.environ.get('RABBIT_VHOST', 'my_vhost')
rabbit_queue = os.environ.get('RABBIT_QUEUE', 'coordinates_to_process')
rabbit_url = f'amqp://{rabbit_user}:{rabbit_password}@{rabbit_host}:{rabbit_port}/{rabbit_vhost}'

db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', '13306')
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', 'QweZxc123')
db_name = os.environ.get('DB_NAME', 'ukcodes')
db_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

app = Celery('tasks', broker=rabbit_url, backend="rpc://")

@app.task
def save_to_db(post_codes: list) -> str:

    db = Db(db_url)
    db.create_schema(Base)

    for post_code in post_codes:
        
        coodinate_id = db.insert_coordinate(post_code['query'])
        post_code_id = db.insert_postcode(post_code['result'][0], coodinate_id)
        db.insert_codes(post_code['result'][0]['codes'], post_code_id)

    db.disconnect()   

    return f'{len(post_codes)} postcodes received.'
