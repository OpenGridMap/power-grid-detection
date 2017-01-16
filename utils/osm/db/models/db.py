from peewee import SqliteDatabase
from config import config_params
import os

db_file_path = os.path.join(
    os.path.dirname(__file__),
    os.pardir,
    os.pardir,
    os.pardir,
    'data',
    'osm',
    # config['loc'] + '-datastore.db'
    'datastore.db'
)

db_dir = os.path.dirname(db_file_path)

if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db = SqliteDatabase(db_file_path)
