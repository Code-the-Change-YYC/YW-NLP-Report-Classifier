import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb://localhost:27017")
db = cluster["YWCA_reports"] 
collection = db["scrubbed_reports"]
results = collection.find_one()

print(results)