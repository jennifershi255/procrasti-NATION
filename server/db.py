from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = os.getenv("DB_STRING")
    
    client = MongoClient(CONNECTION_STRING)

    return client['htn2024']

