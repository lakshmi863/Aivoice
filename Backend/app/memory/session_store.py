from app.database.database import db

# Create/Get a 'sessions' collection in MongoDB
sessions_collection = db.get_collection("sessions")

async def save_user_context(user_id: str, context_data: dict):
    """
    Saves or updates short-term user preferences (like language) in MongoDB.
    Using 'upsert' ensures it creates a new record if the user doesn't exist.
    """
    try:
        await sessions_collection.update_one(
            {"user_id": user_id},
            {"$set": context_data},
            upsert=True
        )
        print(f"✅ Session saved for user: {user_id}")
    except Exception as e:
        print(f"❌ Failed to save session: {e}")

async def get_user_context(user_id: str):
    """
    Retrieves current session context from MongoDB Atlas.
    Defaults to English if no preference is found.
    """
    try:
        session = await sessions_collection.find_one({"user_id": user_id})
        if session:
            return session
        return {"language": "English"}
    except Exception as e:
        print(f"❌ Failed to get session: {e}")
        return {"language": "English"}