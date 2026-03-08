import os
import json
import traceback
from datetime import datetime, timedelta
from groq import Groq
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import TOOLS, AVAILABLE_FUNCTIONS
from app.memory.persistence import get_patient_history

# Initialize the Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def run_conversation(user_input, history=[], patient_id="test_user"):
    # 1. Get exact current time (Informs the LLM of 'today' or 'now')
    now_dt = datetime.now()
    current_time_str = now_dt.strftime("%Y-%m-%d %H:%M (%A)")

    # 2. Fetch persistent history (UPDATED: Make sure this function is async)
    try:
        # Since we are moving to MongoDB, your persistence fetch should be awaited
        past_info = await get_patient_history(patient_id)
    except:
        past_info = "New patient. No previous appointments found."

    # 3. Prepare the Prompt with Time Awareness
    full_system_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"CURRENT_TIME: {current_time_str}\n"
        f"PATIENT_HISTORY: {past_info}\n"
        "REMINDER: Do not suggest appointment slots that have already passed relative to CURRENT_TIME."
    )

    messages = [
        {"role": "system", "content": full_system_prompt},
        *history,
        {"role": "user", "content": user_input}
    ]

    try:
        # 4. First Call: Reasoning (Decide if a Tool call is needed)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # 5. Handle standard chat (If no tool is needed)
        if not tool_calls:
            return response_message.content

        # 6. Execute Async Tool Calls
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Default fallback for empty dates
            if "requested_time" not in function_args and function_name == "check_availability":
                tomorrow = (now_dt + timedelta(days=1)).strftime("%Y-%m-%d 10:00")
                function_args["requested_time"] = tomorrow

            if function_name in AVAILABLE_FUNCTIONS:
                print(f"DEBUG: Triggering tool {function_name} via MongoDB...")
                
                # --- CRITICAL FIX: ADDED 'await' FOR ASYNC MONGODB FUNCTIONS ---
                function_to_call = AVAILABLE_FUNCTIONS[function_name]
                tool_result = await function_to_call(**function_args)
                
                # Format for the LLM
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(tool_result),
                })

        # 7. Second Call: Voice Response (Generate the final natural speech)
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        return final_response.choices[0].message.content

    except Exception as e:
        print("--- ASYNC AGENT ERROR ---")
        print(traceback.format_exc())
        return "I'm having a little trouble connecting to my database right now. Let me try again in a moment."