from dotenv import load_dotenv
import os
from os import getenv

load_dotenv()

PORT = int(os.getenv("PORT"))
POSTGRES_URL = os.getenv("POSTGRES_URL") + '?sslmode=require'

# Local database
POSTGRES_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    getenv('DB_USER'), getenv('DB_PASS'), getenv('DB_HOST'), getenv('DB_PORT'), getenv('DB_NAME')
)

# Flask app
SECRET_KEY = os.getenv("SECRET_KEY")