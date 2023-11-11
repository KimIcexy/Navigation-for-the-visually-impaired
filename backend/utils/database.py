import psycopg2
from psycopg2 import extras
from .config import *

class Database:
    """Manage connections and perform queries to the database.
    
    Attributes:
        uri: the database uri.
        _connection: a connection to the database.
    """
    
    def __init__(self) -> None:
        self.uri = POSTGRES_URL
        self._connection = None
        
    def connect(self):
        """Return a connection to the database."""
        if not self._connection or self._connection.closed:
            # create a connection to the database that can query by column name
            self._connection = psycopg2.connect(self.uri, cursor_factory=extras.RealDictCursor)
        return self._connection
    
    def close(self):
        """Close the connection to the database"""
        if self._connection and not self._connection.closed:
            self._connection.close()
            
    def execute_query(self, query, params = None):
        """Excecute a query to the database and return the result.
        
        Args:
            query: a SQL query command (ex: query = 'SELECT * FROM users')
            params: a tuple params passed to the query command (ex: params = (user_id))
        Returns:
            result: result of the executed query
        """
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result