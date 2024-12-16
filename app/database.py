import os
from pymongo import MongoClient

mongo_port = int(os.getenv("MONGO_PORT", 27017))
client = MongoClient(host="mongo", port=mongo_port)

db = client["scd_hw2"]

