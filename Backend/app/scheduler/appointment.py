from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.database.models import Doctor, Appointment
from datetime import datetime, timedelta

def check_availability(doctor_type: str, requested_time: str):
    """
    Checks if a doctor/specialty is available at a specific time.
    Blocks checks for past dates.
    """
    db = SessionLocal()
    try:
        # 1. PARSE TIME AND VALIDATE
        try:
            appt_time = datetime.strptime(requested_time, "%Y-%m-%d %H:%M")
        except:
            return {"available": False, "message": "The time format is invalid. Please use YYYY-MM-DD HH:MM."}

        # BLOCK PAST DATES
        if appt_time < datetime.now():
            return {
                "available": False, 
                "message": f"I'm sorry, {requested_time} has already passed. Please suggest a future time."
            }

        # 2. SEARCH DOCTOR BY NAME OR SPECIALTY
        doctor = db.query(Doctor).filter(
            or_(
                Doctor.specialty.ilike(f"%{doctor_type}%"),
                Doctor.name.ilike(f"%{doctor_type}%")
            )
        ).first()
        
        if not doctor:
            return {"available": False, "message": f"Sorry, I couldn't find a doctor or specialty matching '{doctor_type}'."}

        # 3. CONFLICT DETECTION
        conflict = db.query(Appointment).filter(
            Appointment.doctor_id == doctor.id,
            Appointment.appointment_time == appt_time,
            Appointment.status == "Scheduled"
        ).first()

        if conflict:
            alt_time = appt_time + timedelta(hours=1)
            return {
                "available": False, 
                "message": f"Dr. {doctor.name} is busy at {requested_time}. Is {alt_time.strftime('%H:%M')} okay?"
            }

        return {
            "available": True, 
            "doctor_name": doctor.name, 
            "message": f"Dr. {doctor.name} ({doctor.specialty}) is available at {requested_time}."
        }
    finally:
        db.close()

def book_appointment(patient_name: str, doctor_type: str, time_str: str, language: str = "en"):
    """
    Finalizes the booking. Saves the language used to persistent memory.
    """
    db = SessionLocal()
    try:
        # 1. VALIDATE TIME
        appt_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        if appt_time < datetime.now():
            return {
                "status": "error", 
                "message": "I cannot confirm this booking because the time has already passed."
            }

        # 2. FIND DOCTOR
        doctor = db.query(Doctor).filter(
            or_(Doctor.specialty.ilike(f"%{doctor_type}%"), Doctor.name.ilike(f"%{doctor_type}%"))
        ).first()

        if not doctor:
            return {"status": "error", "message": "Doctor not found."}

        # 3. SAVE TO DATABASE
        new_appt = Appointment(
            patient_id=patient_name,
            doctor_id=doctor.id,
            appointment_time=appt_time,
            status="Scheduled",
            language=language
        )
        db.add(new_appt)
        db.commit()

        # 4. MULTILINGUAL GREETINGS
        greetings = {
            "en": f"Great {patient_name}! Your appointment with Dr. {doctor.name} is confirmed for {time_str}. Stay healthy!",
            "hi": f"नमस्ते {patient_name}, आपकी अपॉइंटமெंट डॉ. {doctor.name} के साथ {time_str} बजे कन्फर्म हो गई है। अपना ख्याल रखें!",
            "ta": f"வணக்கம் {patient_name}, டாக்டர் {doctor.name} உடனான உங்கள் சந்திப்பு {time_str} மணிக்கு உறுதி செய்யப்பட்டது. நலமுடன் இருங்கள்!"
        }

        return {"status": "success", "message": greetings.get(language, greetings["en"])}

    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

def reschedule_appointment(old_time_str: str, new_time_str: str, patient_name: str = "test_user"):
    """
    Moves an existing appointment to a new slot.
    """
    db = SessionLocal()
    try:
        # 1. Parse and Validate Times
        old_time = datetime.strptime(old_time_str, "%Y-%m-%d %H:%M")
        new_time = datetime.strptime(new_time_str, "%Y-%m-%d %H:%M")

        if new_time < datetime.now():
            return {"status": "error", "message": "The new requested time has already passed."}

        # 2. Find the original appointment
        appt = db.query(Appointment).filter(
            Appointment.patient_id == patient_name,
            Appointment.appointment_time == old_time,
            Appointment.status == "Scheduled"
        ).first()

        if not appt:
            return {"status": "error", "message": f"I couldn't find a scheduled appointment at {old_time_str}."}

        # 3. Check for conflict in the NEW slot
        conflict = db.query(Appointment).filter(
            Appointment.doctor_id == appt.doctor_id,
            Appointment.appointment_time == new_time,
            Appointment.status == "Scheduled"
        ).first()

        if conflict:
            return {"status": "error", "message": "Sorry, that new slot is already booked. Please choose another time."}

        # 4. Perform Update
        appt.appointment_time = new_time
        db.commit()
        return {"status": "success", "message": f"Successfully rescheduled. Your new time is {new_time_str}."}

    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

def cancel_appointment(time_str: str, patient_name: str = "test_user"):
    """
    Marks an appointment as Cancelled.
    """
    db = SessionLocal()
    try:
        appt_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        appt = db.query(Appointment).filter(
            Appointment.appointment_time == appt_time,
            Appointment.status == "Scheduled"
        ).first()

        if not appt:
            return {"status": "error", "message": "No scheduled appointment found for that time."}

        appt.status = "Cancelled"
        db.commit()
        return {"status": "success", "message": "Your appointment has been successfully cancelled. Take care."}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()