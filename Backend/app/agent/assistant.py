import os
import json
import traceback
from datetime import datetime, timedelta
from groq import Groq
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import TOOLS, AVAILABLE_FUNCTIONS
from app.memory.persistence import get_patient_history

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def run_conversation(user_input, history=[], patient_id="test_user"):
    now_dt = datetime.now()
    current_time_str = now_dt.strftime("%Y-%m-%d %H:%M (%A)")

    try:
        past_info = await get_patient_history(patient_id)
    except:
        past_info = "New patient."

    full_system_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"CURRENT_TIME: {current_time_str}\n"
        f"PATIENT_HISTORY: {past_info}\n"
        "RECAP: Speak English, Hindi, or Tamil as requested. Concisely (< 20 words)."
    )

    messages = [
        {"role": "system", "content": full_system_prompt},
        *history,
        {"role": "user", "content": user_input}
    ]

    try:
        # --- FIX: Changed decommissioned model to llama-3.1-8b-instant ---
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if not tool_calls:
            return response_message.content

        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if "requested_time" not in function_args and function_name == "check_availability":
                function_args["requested_time"] = (now_dt + timedelta(days=1)).strftime("%Y-%m-%d 10:00")

            if function_name in AVAILABLE_FUNCTIONS:
                function_to_call = AVAILABLE_FUNCTIONS[function_name]
                tool_result = await function_to_call(**function_args)
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(tool_result),
                })

        # --- FIX: Changed decommissioned model here as well ---
        final_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        return final_response.choices[0].message.content

    except Exception as e:
        print("--- LLM ERROR ---")
        print(traceback.format_exc())
        return "I experienced a brief logic error. Please try your request again!"