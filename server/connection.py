from pymongo import MongoClient
import settings

client = MongoClient(settings.mongo_url_local)

# for local connection
db =client['YWCA_reports']
collection = db['scrubbed_reports']

# for mongo altas
# db =client['YWCA_CIR']
# collection = db['YWCA_2020_05_02']


# testing connection 
if collection.find({"Form - Client Involved - Primary (initials)":"RT"}): print("find RT")
    