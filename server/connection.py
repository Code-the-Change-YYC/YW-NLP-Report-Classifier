from server.credentials import Credentials
from pymongo import MongoClient

# TODO: Update to use global `credentials` object after PR #65
mongo_url = Credentials().mongo_url

client = MongoClient(mongo_url)

# for local connection
db =client['YWCA_reports']
collection = db['test_report']

# for mongo altas
# db =client['YWCA_CIR']
# collection = db['YWCA_2020_05_02']


