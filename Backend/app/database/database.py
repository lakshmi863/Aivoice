import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load local .env file if it exists
load_dotenv()

# 1. Force retrieval of DATABASE_URL
# On Render, this must be set in the 'Environment' tab
MONGO_URL = os.getenv("DATABASE_URL")

# 2. Safety Logic: Check if we are on Render or Local
if not MONGO_URL:
    # This print will show up in your Render Logs if you forgot to set the Env Var
    print("⚠️ WARNING: DATABASE_URL not found in environment!")
    print("🏠 Falling back to local MongoDB for development...")
    MONGO_URL = "mongodb://localhost:27017"
else:
    # Hide password in logs for security
    sanitized_url = MONGO_URL.split("@")[-1] if "@" in MONGO_URL else "URL Found"
    print(f"🌍 System detected MongoDB Cloud Cluster: ...@{sanitized_url}")

# 3. Create the Client and Database
# Using 'retryWrites=true' and 'w=majority' is recommended for Atlas Clusters
client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database("2care_ai")

# 4. Collections
# We export these so all other files (persistence, appointment) use the SAME connection
doctors_collection = db.get_collection("doctors")
appointments_collection = db.get_collection("appointments")
sessions_collection = db.get_collection("sessions")

# 5. Connection Test
async def test_mongo_connection():
    try:
        # Use a short timeout for the ping test (2 seconds)
        await asyncio.wait_for(client.admin.command('ping'), timeout=2.0)
        print("✅ CONNECTION SUCCESS: Successfully connected to MongoDB Atlas Cluster!")
    except asyncio.TimeoutError:
        print("❌ CONNECTION TIMEOUT: Could not reach MongoDB. Is the IP Whitelisted?")
    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")