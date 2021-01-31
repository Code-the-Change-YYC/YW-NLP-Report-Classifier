from server.credentials import Credentials
from pymongo import MongoClient

# TODO: Update to use global `credentials` object after PR #65
mongo_url = Credentials().mongo_url
client = MongoClient(mongo_url)
db = client['YWCA_reports']
collection = db['test_report']
