from pymongo import MongoClient
from fastapi import Depends
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["realestate"]

def get_listing_collection():
    return db["listings"]
