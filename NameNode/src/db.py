import os 
from pymongo import MongoClient

class MongoDBClient:
    def __init__(self):
        uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(uri)
        self.db = self.client.get_database()

    def save_metadata(self, archivo):
        self.db.archivos.insert_one(archivo)
