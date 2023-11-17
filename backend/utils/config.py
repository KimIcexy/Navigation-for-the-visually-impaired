from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv("PORT"))
POSTGRES_URL = os.getenv("POSTGRES_URL") + '?sslmode=require'