from app.database.database import appointments_collection

async def get_patient_history(patient_id: str):
    """
    Retrieves all past interactions/appointments from MongoDB Atlas.
    Allows the AI to say: 'Welcome back, I see you saw Dr. Sharma last month.'
    """
    try:
        # 1. Search the MongoDB 'appointments' collection
        # We find all appointments for this patient and limit to the last 10
        cursor = appointments_collection.find({"patient_id": patient_id})
        
        # 2. Convert to list (MUST be awaited because it's an async operation)
        history = await cursor.to_list(length=10)
        
        if not history:
            return "New Patient. No previous medical records found."
        
        # 3. Build the text summary for the AI Agent
        summary = []
        for appt in history:
            # Use .get() because MongoDB results are Dictionaries, not SQL Objects
            time = appt.get("appointment_time", "Unknown Time")
            doctor = appt.get("doctor_name", "a specialist")
            status = appt.get("status", "Scheduled")
            
            summary.append(f"Date: {time}, Doctor: {doctor}, Status: {status}")
        
        return " | ".join(summary)

    except Exception as e:
        print(f"❌ Error fetching history from Atlas: {e}")
        return "History retrieval failed. Treating as New Patient."