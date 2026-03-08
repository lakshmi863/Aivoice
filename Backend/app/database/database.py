import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Use your MongoDB Cluster URL from Environment Variables
# Format: mongodb+srv://<user>:<password>@cluster.mongodb.net/dbname
MONGO_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database("2care_ai")

# Collections
doctors_collection = db.get_collection("doctors")
appointments_collection = db.get_collection("appointments")

# Helper to test connection
async def test_mongo_connection():
    try:
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Cluster!")
    except Exception as e:
        print(f"❌ MongoDB Connection Error: {e}")