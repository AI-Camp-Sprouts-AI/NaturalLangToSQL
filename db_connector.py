# Connect to the hosted DB and return the connection
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    connection = psycopg2.connect(DATABASE_URL)
    return connection