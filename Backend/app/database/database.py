import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Check exactly what variable is being seen
MONGO_URL = os.environ.get("DATABASE_URL")

if not MONGO_URL:
    # On Render, if you see this in the logs, the environment variable is MISSING.
    print("FATAL ERROR: DATABASE_URL is NOT set on Render Dashboard!")
    MONGO_URL = "mongodb://localhost:27017" # Fallback (local only)
else:
    print(f"DEBUG: Found Cloud URL: {MONGO_URL[:20]}...") 

client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database("2care_ai")

doctors_collection = db.get_collection("doctors")
appointments_collection = db.get_collection("appointments")
sessions_collection = db.get_collection("sessions")

async def test_mongo_connection():
    try:
        # standard ping with a 5 second limit
        await asyncio.wait_for(client.admin.command('ping'), timeout=5.0)
        print("✅ MongoDB Cluster Connected!")
    except Exception as e:
        print(f"❌ Connection check failed: {e}")