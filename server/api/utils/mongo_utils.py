from pymongo import MongoClient
from django.conf import settings

def get_mongo_db():
    client = MongoClient(settings.MONGO_CONFIG['host'])
    return client[settings.MONGO_CONFIG['dbname']]
