import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# --- Define the Tool ---
def get_weather(location):
    """Mock function to simulate a weather API"""
    if "New York" in location:
        return json.dumps({"location": "New York", "temperature": "72", "unit": "fahrenheit"})
    elif "London" in location:
        return json.dumps({"location": "London", "temperature": "15", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
            },
            "required": ["location"],
        },
    }
}]

# --- Execution ---
messages = [{"role": "user", "content": "What's the weather like in London?"}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

tool_calls = response.choices[0].message.tool_calls

if tool_calls:
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        if function_name == "get_weather":
            function_response = get_weather(location=function_args.get("location"))
            
            # Append tool response to conversation
            messages.append(response.choices[0].message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": function_response,
            })

    # Get final answer from model
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    print(final_response.choices[0].message.content)
