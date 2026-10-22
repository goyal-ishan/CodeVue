import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = (
    os.getenv("INTERVIEW_MONGO_URI")
    or os.getenv("MONGO_URI")
    or os.getenv("MONGODB_URI")
    or "mongodb://localhost:27017"
)

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
)

db = client["codevue_interviews"]
interviews_collection = db["interviews"]


def check_mongodb_connection():
    client.admin.command("ping")
    print("Interview MongoDB connected successfully")