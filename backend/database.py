from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "smart_nutrition_tracker"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_database():
    return db
