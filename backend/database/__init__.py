from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import utils.config as config

class Database:
    '''
    Database class for SQLAlchemy. Manage connections and perform actions.

    Attributes:
        url: the database uri.
        engine: the database engine.
        _session: a connection to the database.
        Base: the declarative base for the database. For creating models.
    '''
    def __init__(self):
        print('Initializing database...')
        self.url = config.POSTGRES_URL
        self.engine = create_engine(self.url)
        self._session = None
        self.Base = declarative_base()

    def init_db(self):
        '''Initialize the database.'''
        print('Initializing database tables...')
        self.Base.metadata.create_all(self.engine)

    def connect(self):
        '''Return a connection to the database.'''
        if not self._session:
            Session = sessionmaker(bind=self.engine)
            self._session = Session()

        return self._session
    
    def close(self):
        '''Close the connection to the database'''
        if self._session:
            self._session.close()

        return True

    def query(self, model, filters):
        '''Query the database.'''
        session = self.connect()
        query = session.query(model)
        for key, value in filters.items():
            query = query.filter(getattr(model, key) == value)

        self.close()
        return query.all()
    
    def save(self, obj):
        '''Save an object to the database.'''
        session = self.connect()
        session.add(obj)
        session.commit()
        self.close()

    def delete(self, obj):
        '''Delete an object from the database.'''
        session = self.connect()
        session.delete(obj)
        session.commit()
        self.close()

    def edit(self, obj, **kwargs):
        '''Edit an object from the database.'''
        session = self.connect()
        for key, value in kwargs.items():
            setattr(obj, key, value)
        session.add(obj)
        session.commit()
        self.close()

    def rollback(self):
        '''Rollback the database.'''
        session = self.connect()
        session.rollback()
        self.close()

db = Database()