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
    # 1. Get exact current time to make the AI 'Time-Aware'
    now_dt = datetime.now()
    current_time_str = now_dt.strftime("%Y-%m-%d %H:%M (%A)")

    # 2. Fetch persistent history 
    try:
        past_info = get_patient_history(patient_id)
    except:
        past_info = "New patient."

    # 3. Prepare Context with Current Time (Fixes the "2024" and "Past Date" issues)
    full_system_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"CURRENT_TIME: {current_time_str}\n"
        f"PATIENT_HISTORY: {past_info}\n"
        "INSTRUCTION: Use the current time to validate 'today' or 'now' requests. "
        "Do not suggest slots that have already passed."
    )

    messages = [
        {"role": "system", "content": full_system_prompt},
        *history,
        {"role": "user", "content": user_input}
    ]

    try:
        # 4. First Call: AI decides if it needs a Tool (Booking/Checking)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # 5. If AI just wants to chat (No Tool needed)
        if not tool_calls:
            return response_message.content

        # 6. Execute Tool Logic
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Smart Logic: If user didn't give a time, suggest tomorrow morning
            if "requested_time" not in function_args and function_name == "check_availability":
                tomorrow = (now_dt + timedelta(days=1)).strftime("%Y-%m-%d 10:00")
                function_args["requested_time"] = tomorrow

            if function_name in AVAILABLE_FUNCTIONS:
                print(f"DEBUG: AI triggering {function_name} with {function_args}")
                
                # Execute the actual database function
                function_to_call = AVAILABLE_FUNCTIONS[function_name]
                tool_result = function_to_call(**function_args)
                
                # Send the database result back to the AI
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(tool_result),
                })

        # 7. Second Call: AI turns technical DB result into a natural response
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        return final_response.choices[0].message.content

    except Exception as e:
        print("--- LLM ERROR ---")
        print(traceback.format_exc())
        return "I'm sorry, I'm having trouble connecting to the medical scheduler right now. Please try again in a moment."