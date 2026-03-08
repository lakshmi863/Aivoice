import asyncio
from app.database.database import SessionLocal
from app.database.models import Appointment

async def trigger_reminder_campaign():
    """
    Finds upcoming appointments and simulates a reminder call.
    In a real app, this would trigger a Twilio call or WebSocket push.
    """
    db = SessionLocal()
    # Mocking: finding appointments for today
    reminders = db.query(Appointment).filter(Appointment.status == "Scheduled").all()
    
    for entry in reminders:
        print(f"OUTBOUND CALL to {entry.patient_id}: 'Hi, you have an appointment with Dr. {entry.doctor_id} tomorrow.'")
    
    db.close()