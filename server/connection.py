from server.credentials import credentials
from pymongo import MongoClient

mongo_url = credentials.mongo_url if credentials.PYTHON_ENV == 'development' else 'mongodb://mongo:27017'
client = MongoClient(mongo_url)
db = client['YWCA_reports']
collection = db['test_report']
