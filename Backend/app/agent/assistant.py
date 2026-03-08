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
    # 1. Get exact current time to make AI time-aware
    now_dt = datetime.now()
    current_time_str = now_dt.strftime("%Y-%m-%d %H:%M (%A)")

    # 2. Fetch persistent history (Async MongoDB fetch)
    try:
        # Crucial: Must 'await' history retrieval from MongoDB Cluster
        past_info = await get_patient_history(patient_id)
    except:
        past_info = "New patient. No history found."

    # 3. Build Full Context
    # Telling the AI to be concise (< 20 words) for low voice latency
    full_system_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"CURRENT_TIME: {current_time_str}\n"
        f"PATIENT_HISTORY: {past_info}\n"
        "RECAP: Always respond in the user's language. Keep answers under 20 words."
    )

    messages = [
        {"role": "system", "content": full_system_prompt},
        *history,
        {"role": "user", "content": user_input}
    ]

    try:
        # 4. First Call: Use llama3-8b-8192 for lower latency and higher rate limits
        response = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # 5. Natural Chat handling (No tool needed)
        if not tool_calls:
            return response_message.content

        # 6. Async Tool Execution Logic
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Dynamic default time logic
            if "requested_time" not in function_args and function_name == "check_availability":
                function_args["requested_time"] = (now_dt + timedelta(days=1)).strftime("%Y-%m-%d 10:00")

            if function_name in AVAILABLE_FUNCTIONS:
                print(f"DEBUG: Triggering Cloud DB Tool: {function_name}")
                
                # --- ASYNC EXECUTION FOR MONGODB ---
                function_to_call = AVAILABLE_FUNCTIONS[function_name]
                tool_result = await function_to_call(**function_args)
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(tool_result),
                })

        # 7. Final Response Generation (Speech output)
        final_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )
        return final_response.choices[0].message.content

    except Exception as e:
        print("--- AGENT SYSTEM ERROR ---")
        print(traceback.format_exc())
        return "I'm experiencing a brief connection issue. Could you please try again?"