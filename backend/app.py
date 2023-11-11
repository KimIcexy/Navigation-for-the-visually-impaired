from flask import Flask
import os
import psycopg2

from utils.config import *
from utils.database import Database

app = Flask(__name__)
database = Database()

@app.route('/')
def home():
    try:
        database_connection = database.connect()
        return 'Hello, you have connected to the database~~~'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True, port=PORT)