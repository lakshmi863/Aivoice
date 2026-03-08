from datetime import datetime, timedelta
from app.database.database import doctors_collection, appointments_collection

async def check_availability(doctor_type: str, requested_time: str):
    """
    Checks MongoDB for doctors by Name OR Specialty.
    Blocks past dates and detects conflicts.
    """
    try:
        # 1. PARSE AND VALIDATE TIME
        appt_time = datetime.strptime(requested_time, "%Y-%m-%d %H:%M")
        if appt_time < datetime.now():
            return {
                "available": False, 
                "message": f"I'm sorry, {requested_time} has already passed. Please suggest a future date."
            }

        # 2. SEARCH DOCTOR (Case-insensitive Regex for Name or Specialty)
        doctor = await doctors_collection.find_one({
            "$or": [
                {"specialty": {"$regex": f"^{doctor_type}$", "$options": "i"}},
                {"name": {"$regex": doctor_type, "$options": "i"}}
            ]
        })

        if not doctor:
            # Try a broader search if exact match fails
            doctor = await doctors_collection.find_one({
                "specialty": {"$regex": doctor_type, "$options": "i"}
            })

        if not doctor:
            return {"available": False, "message": f"I couldn't find a doctor or specialty matching '{doctor_type}'."}

        # 3. CONFLICT DETECTION (Look for existing scheduled appts at this exact time)
        conflict = await appointments_collection.find_one({
            "doctor_id": doctor["_id"],
            "appointment_time": appt_time,
            "status": "Scheduled"
        })

        if conflict:
            alt_time = appt_time + timedelta(hours=1)
            return {
                "available": False, 
                "message": f"Dr. {doctor['name']} is busy then. Is {alt_time.strftime('%H:%M')} okay?"
            }

        return {
            "available": True, 
            "doctor_name": doctor["name"], 
            "message": f"Dr. {doctor['name']} is available at {requested_time}."
        }
    except Exception as e:
        return {"available": False, "message": f"System error: {str(e)}"}

async def book_appointment(patient_name: str, doctor_type: str, time_str: str, language: str = "en"):
    """
    Saves a new appointment to the MongoDB Atlas Cluster.
    """
    try:
        # 1. DATE VALIDATION
        appt_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        if appt_time < datetime.now():
            return {"status": "error", "message": "Cannot book a time that has already passed."}
        
        # 2. FIND DOCTOR TO GET ID
        doctor = await doctors_collection.find_one({
            "$or": [
                {"specialty": {"$regex": doctor_type, "$options": "i"}},
                {"name": {"$regex": doctor_type, "$options": "i"}}
            ]
        })

        if not doctor:
            return {"status": "error", "message": "Doctor not found."}

        # 3. CREATE DOCUMENT
        new_appt = {
            "patient_id": patient_name,
            "doctor_id": doctor["_id"],
            "doctor_name": doctor["name"],
            "appointment_time": appt_time,
            "status": "Scheduled",
            "language": language,
            "created_at": datetime.now()
        }

        await appointments_collection.insert_one(new_appt)

        # 4. MULTILINGUAL GREETINGS
        greetings = {
            "en": f"Confirmed! You are scheduled with Dr. {doctor['name']} at {time_str}. Stay healthy!",
            "hi": f"कन्फर्म है! आप {time_str} बजे डॉ. {doctor['name']} से मिल रहे हैं। अपना ख्याल रखें!",
            "ta": f"உறுதி செய்யப்பட்டது! நீங்கள் {time_str} மணிக்கு டாக்டர் {doctor['name']}-ஐ சந்திக்கலாம். நலமுடன் இருங்கள்!"
        }

        return {"status": "success", "message": greetings.get(language, greetings["en"])}
    except Exception as e:
        return {"status": "error", "message": f"Failed to book: {str(e)}"}

async def reschedule_appointment(old_time_str: str, new_time_str: str, patient_name: str = "test_user"):
    """
    Updates an existing appointment in MongoDB.
    """
    try:
        old_time = datetime.strptime(old_time_str, "%Y-%m-%d %H:%M")
        new_time = datetime.strptime(new_time_str, "%Y-%m-%d %H:%M")

        if new_time < datetime.now():
            return {"status": "error", "message": "New time cannot be in the past."}

        # Find the original record
        appt = await appointments_collection.find_one({
            "patient_id": patient_name,
            "appointment_time": old_time,
            "status": "Scheduled"
        })

        if not appt:
            return {"status": "error", "message": "No existing appointment found at that time."}

        # Update the record
        await appointments_collection.update_one(
            {"_id": appt["_id"]},
            {"$set": {"appointment_time": new_time}}
        )

        return {"status": "success", "message": f"Successfully moved your appointment to {new_time_str}."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def cancel_appointment(time_str: str, patient_name: str = "test_user"):
    """
    Marks an appointment as Cancelled in MongoDB.
    """
    try:
        appt_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        result = await appointments_collection.update_one(
            {
                "patient_id": patient_name,
                "appointment_time": appt_time,
                "status": "Scheduled"
            },
            {"$set": {"status": "Cancelled"}}
        )

        if result.matched_count == 0:
            return {"status": "error", "message": "No scheduled appointment found to cancel."}

        return {"status": "success", "message": "Successfully cancelled. Take care!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}