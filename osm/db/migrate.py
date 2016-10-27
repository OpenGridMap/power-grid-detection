import os

from osm.db.models import db, PowerTag, DataPoint, db_file_path


def create_tables():
    db.connect()
    db.create_tables([PowerTag, DataPoint], safe=True)


if __name__ == '__main__':
    if not os.path.isfile(db_file_path):
        create_tables()
