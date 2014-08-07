import os
from config import BaseConfig
from app import app, init_db

if __name__ == '__main__':
    base_config = BaseConfig()
    db_uri = base_config.DATABASE_URI

    if not os.path.isfile(db_uri):
        init_db()

    app.run()
