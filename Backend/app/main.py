from dotenv import load_dotenv
load_dotenv() 

import uvicorn
import logging
from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database.database import engine, Base, SessionLocal
from app.database import models
from app.database.models import Doctor # Import Doctor model
from app.websocket import router as ws_router

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("2CareMain")

# 2. Initialize Database Tables
logger.info("Creating database tables...")
Base.metadata.create_all(bind=engine)

# 3. AUTO-SEEDER: Ensure doctors exist in the database (Crucial for Render)
def seed_database():
    db: Session = SessionLocal()
    try:
        doctor_count = db.query(Doctor).count()
        if doctor_count == 0:
            logger.info("Database is empty. Seeding initial doctors...")
            initial_doctors = [
                Doctor(name="Arjun Sharma", specialty="Cardiologist"),
                Doctor(name="Priya Nair", specialty="Dermatologist"),
                Doctor(name="Suresh Iyer", specialty="Neurologist"),
                Doctor(name="Kavita Reddy", specialty="Pediatrician"),
                Doctor(name="Anjali Gupta", specialty="Gynecologist")
            ]
            db.add_all(initial_doctors)
            db.commit()
            logger.info(f"Successfully seeded {len(initial_doctors)} doctors.")
        else:
            logger.info(f"Database already has {doctor_count} doctors. Skipping seed.")
    except Exception as e:
        logger.error(f"Seeding error: {e}")
        db.rollback()
    finally:
        db.close()

# Run the seeder before the app starts
seed_database()

# 4. FastAPI Setup
app = FastAPI(title="2Care.ai Voice AI Agent")

# Include the Voice WebSocket Router
app.include_router(ws_router)

@app.get("/")
async def root():
    return {
        "message": "2Care.ai Real-Time Voice API is Running",
        "status": "Healthy"
    }

@app.post("/campaign/remind")
async def trigger_reminders():
    from app.scheduler.outbound import trigger_reminder_campaign
    await trigger_reminder_campaign()
    return {"status": "Reminders triggered"}

if __name__ == "__main__":
    # Render uses the $PORT env variable. Default to 8000 for local dev.
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)