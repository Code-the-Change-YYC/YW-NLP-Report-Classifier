from server.credentials import credentials
from pymongo import MongoClient

mongo_url = credentials.mongo_url
client = MongoClient(mongo_url)
db = client['YWCA_reports']
collection = db['test_report']
