from pymongo import MongoClient

mongo_url_local = "mongodb://localhost:27017"

client = MongoClient(mongo_url_local)

# for local connection
db =client['YWCA_reports']
collection = db['test_report']

# for mongo altas
# db =client['YWCA_CIR']
# collection = db['YWCA_2020_05_02']


