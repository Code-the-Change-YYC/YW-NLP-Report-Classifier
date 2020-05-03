# import the MongoClient from the pymongo library
from pymongo import MongoClient

# get the client object from this class and connect to the local instance
client = MongoClient("mongodb://localhost:27017/")

# Get database by name
db = client["yw-reports"]
reports = db["reports"]

print(reports.find_one())
