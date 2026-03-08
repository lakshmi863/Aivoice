from app.database.database import SessionLocal
from app.database.models import Appointment

def get_patient_history(patient_id: str):
    """
    Retrieves all past interactions/appointments for a specific patient.
    Allows the AI to say: 'Welcome back, I see you saw Dr. Sharma last month.'
    """
    db = SessionLocal()
    history = db.query(Appointment).filter(Appointment.patient_id == patient_id).all()
    db.close()
    
    if not history:
        return "New Patient"
    
    summary = []
    for appt in history:
        summary.append(f"Date: {appt.appointment_time}, Doctor: {appt.doctor_id}, Status: {appt.status}")
    
    return " | ".join(summary)