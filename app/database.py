from pymongo import MongoClient
from app.settings import mongodb_uri

client = MongoClient(mongodb_uri)

db = client.Copilot

poi = db.poi
data = db.data
users = db.users


