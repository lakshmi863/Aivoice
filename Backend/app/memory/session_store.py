# Simple In-Memory Cache (In production, use Redis)
user_preferences = {}

def save_user_context(user_id: str, context_data: dict):
    if user_id not in user_preferences:
        user_preferences[user_id] = {}
    user_preferences[user_id].update(context_data)

def get_user_context(user_id: str):
    return user_preferences.get(user_id, {"language": "English"})