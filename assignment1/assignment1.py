from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["accident_report_data"]["accident_report_data"]

print(db.find_one())
