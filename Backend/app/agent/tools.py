from app.scheduler.appointment import book_appointment, check_availability, cancel_appointment, reschedule_appointment

# Define the tools for the LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check if a specific doctor/specialty is available at a specific time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_type": {"type": "string", "description": "e.g. Cardiologist"},
                    "requested_time": {"type": "string", "description": "Format: YYYY-MM-DD HH:MM"}
                },
                "required": ["doctor_type", "requested_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book a clinical appointment for a patient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_name": {"type": "string"},
                    "doctor_type": {"type": "string"},
                    "time_str": {"type": "string", "description": "YYYY-MM-DD HH:MM"}
                },
                "required": ["patient_name", "doctor_type", "time_str"]
            }
        }
    },
    

    {
    "type": "function",
    "function": {
        "name": "cancel_appointment",
        "description": "Cancel an existing clinical appointment.",
        "parameters": {
            "type": "object",
            "properties": {
                "time_str": {"type": "string", "description": "Format: YYYY-MM-DD HH:MM"},
                "patient_name": {"type": "string"}
            },
            "required": ["time_str"]
        }
    }
}
,

{
    "type": "function",
    "function": {
        "name": "reschedule_appointment",
        "description": "Change an existing appointment to a new date and time.",
        "parameters": {
            "type": "object",
            "properties": {
                "old_time_str": {"type": "string", "description": "Current time of appt. YYYY-MM-DD HH:MM"},
                "new_time_str": {"type": "string", "description": "New time desired. YYYY-MM-DD HH:MM"},
                "patient_name": {"type": "string"}
            },
            "required": ["old_time_str", "new_time_str"]
        }
    }
}
]
# IMPORTANT: Also update AVAILABLE_FUNCTIONS at the bottom of the same file
AVAILABLE_FUNCTIONS = {
    "check_availability": check_availability,
    "book_appointment": book_appointment,
    "cancel_appointment": cancel_appointment,
    "reschedule_appointment": reschedule_appointment
}