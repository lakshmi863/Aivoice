# 1. First: Load variables from .env
from dotenv import load_dotenv
load_dotenv() 

# 2. Second: Now import everything else
import uvicorn
from fastapi import FastAPI
from app.database.database import engine, Base
from app.database import models
from app.websocket import router as ws_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="2Care.ai Voice AI Agent")
app.include_router(ws_router)

@app.get("/")
async def root():
    return {"message": "2Care.ai Real-Time Voice API is Running"}

@app.post("/campaign/remind")
async def trigger_reminders():
    from app.scheduler.outbound import trigger_reminder_campaign
    await trigger_reminder_campaign()
    return {"status": "Reminders triggered"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)