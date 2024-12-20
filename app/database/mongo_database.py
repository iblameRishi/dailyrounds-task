from pymongo import MongoClient

# Initialize connection to MongoDB
client = MongoClient("mongodb://db:27017")
db = client.imdb_task
