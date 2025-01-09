import pymongo
from django.conf import settings

client = pymongo.MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
games_collection = db['games']
