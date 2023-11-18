# SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# .env
import utils.config as config

# Flask
from flask import g

url = config.LOCAL_POSTGRES_URL
engine = create_engine(url)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    if 'db' not in g:
        g.db = Session()

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()