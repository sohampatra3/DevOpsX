import os
import requests
import json
from openai import OpenAI

# ————— CONFIGURATION —————
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("Missing OPENAI_API_KEY environment variable")
client = OpenAI(api_key=API_KEY)
# No API key needed for wttr.in

# ————— WEATHER FUNCTION —————
def get_current_weather(city: str) -> str:
    """
    Fetches current weather for the given city using wttr.in.
    Returns a one-line summary.
    """
    url = f"https://wttr.in/{city}"
    params = {
        "format": "3"  # one-line summary: "City: weather, temperature"
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        return f"Sorry, couldn't fetch weather for {city} (status {resp.status_code})."
    return resp.text.strip()

# Schema definition for function calling
function_schemas = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given city via wttr.in",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city to fetch weather for"
                }
            },
            "required": ["city"],
        },
    }
]

# ————— AGENT LOOP —————
def ask_weather_agent(user_prompt: str):
    # 1) Send user message + function schema
    chat_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_prompt}],
        functions=function_schemas,
        function_call="auto",
    )
    # get the message object
    message = chat_resp.choices[0].message

    # 2) If it's a function call, handle it
    if message.function_call:
        fname = message.function_call.name
        args_str = message.function_call.arguments
        args = json.loads(args_str)

        # Call our local weather function
        weather_str = get_current_weather(**args)

        # 3) Send the function result back to the model
        followup = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_prompt},   
                {
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": fname,
                        "arguments": args_str
                    }
                },
                {"role": "function", "name": fname, "content": weather_str},
            ],
        )
        # 4) Print the agent’s final reply
        print(followup.choices[0].message.content)
    else:
        # If no function was called, just echo
        print(message.content)

if __name__ == "__main__":
    # Prompt user for a city name
    city = input("Enter the city name for the weather query: ")
    # Query the agent using the provided city
    ask_weather_agent(f"What's the weather in {city} right now?")