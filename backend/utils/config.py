from dotenv import load_dotenv
import os
from os import getenv

load_dotenv()

PORT = int(os.getenv("PORT"))
# POSTGRES_URL = os.getenv("POSTGRES_URL") + '?sslmode=require'

# Local database
# Check if .env.local exists
# if os.path.exists('.env.local'):
#     load_dotenv('.env.local')
    
#     LOCAL_POSTGRES_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
#         getenv('DB_USER'), getenv('DB_PASS'), getenv('DB_HOST'), getenv('DB_PORT'), getenv('DB_NAME')
#     )

POSTGRES_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    getenv('DB_USER'), getenv('DB_PASS'), getenv('DB_HOST'), getenv('DB_PORT'), getenv('DB_NAME')
)

# Flask app
SECRET_KEY = os.getenv("SECRET_KEY")