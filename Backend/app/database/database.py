import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Force environment reload
load_dotenv()

# Check what the system sees (will show up in Render logs)
MONGO_URL = os.environ.get("DATABASE_URL")

if MONGO_URL and "localhost" not in MONGO_URL:
    print(f"🌍 SUCCESS: DATABASE_URL detected for Cluster: {MONGO_URL.split('@')[-1]}")
else:
    print("❌ CRITICAL: DATABASE_URL is missing or stuck on localhost!")
    # Temporary fallback if the variable is not propagating
    MONGO_URL = "mongodb://localhost:27017"

# Create the async client
client = AsyncIOMotorClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000, # If it can't connect in 5s, it will fail fast
    connectTimeoutMS=5000
)

db = client.get_database("2care_ai")

doctors_collection = db.get_collection("doctors")
appointments_collection = db.get_collection("appointments")
sessions_collection = db.get_collection("sessions")

async def test_mongo_connection():
    try:
        await asyncio.wait_for(client.admin.command('ping'), timeout=5.0)
        print("✅ DATABASE IS ONLINE: Connected to Atlas Cluster.")
    except Exception as e:
        print(f"❌ DATABASE OFFLINE: {e}")