# 1. First: Load environment variables
from dotenv import load_dotenv
load_dotenv() 

import os
import uvicorn
import logging
import asyncio
from fastapi import FastAPI

# Import MongoDB connection and collections
from app.database.database import doctors_collection, test_mongo_connection
from app.websocket import router as ws_router

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("2CareMain")

# 2. FastAPI Setup
app = FastAPI(title="2Care.ai Voice AI Agent")

# 3. AUTO-SEEDER: Ensure doctors exist in MongoDB Atlas (Crucial for Cloud Persistence)
@app.on_event("startup")
async def startup_event():
    """
    This runs every time the server starts. 
    It checks if the MongoDB Cluster is reachable and seeds the doctor list if empty.
    """
    # Test connection to Atlas
    await test_mongo_connection()

    try:
        # Check if any doctors exist in the collection
        doctor_count = await doctors_collection.count_documents({})
        
        if doctor_count == 0:
            logger.info("MongoDB collection is empty. Seeding initial doctors...")
            initial_doctors = [
                {"name": "Arjun Sharma", "specialty": "Cardiolog"},
                {"name": "Priya Nair", "specialty": "Dermatolog"},
                {"name": "Suresh Iyer", "specialty": "Neurolog"},
                {"name": "Kavita Reddy", "specialty": "Pediatrician"},
                {"name": "Anjali Gupta", "specialty": "Gynecolog"},
                {"name": "Vikram Singh", "specialty": "Orthopedic Surgeon"},
                {"name": "Meenakshi Sundaram", "specialty": "Ophthalmolog"},
                {"name": "Rahul Verma", "specialty": "General Physician"},
                {"name": "Deepa Lakshmi", "specialty": "Psychiatrist"},
                {"name": "Karthik Raja", "specialty": "ENT Specialist"},
                {"name": "Sonia Malhotra", "specialty": "Dentist"},
                {"name": "Abdul Rahim", "specialty": "Urologist"}

           

            ]
            # Use insert_many for high-speed batch insertion
            await doctors_collection.insert_many(initial_doctors)
            logger.info(f"Successfully seeded {len(initial_doctors)} doctors into Atlas.")
        else:
            logger.info(f"MongoDB Atlas already contains {doctor_count} doctors. Ready.")
            
    except Exception as e:
        logger.error(f"Seeding error: {e}")

# 4. Include the Voice WebSocket Router
app.include_router(ws_router)

@app.get("/")
async def root():
    return {
        "message": "2Care.ai Real-Time Voice API is Running on MongoDB Atlas",
        "status": "Healthy"
    }

@app.post("/campaign/remind")
async def trigger_reminders():
    # Keep this for the outbound campaign requirement
    from app.scheduler.outbound import trigger_reminder_campaign
    await trigger_reminder_campaign()
    return {"status": "Reminders triggered"}

if __name__ == "__main__":
    # Render uses the $PORT env variable.
    port = int(os.environ.get("PORT", 8000))
    # Note: 'reload' should be False in production
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
