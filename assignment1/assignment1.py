from pprint import pprint

from pymongo import MongoClient


def print_first_report():
    client = MongoClient(host='localhost', port=27017)
    db = client['yw-reports']
    reports_col = db['reports']
    first_report = reports_col.find_one()
    pprint(first_report)


if __name__ == '__main__':
    print_first_report()
