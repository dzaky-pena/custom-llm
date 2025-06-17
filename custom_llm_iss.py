import asyncio
import json
import traceback
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import time

import aiohttp
import requests
from dotenv import load_dotenv
from flask import Flask, Response, request, stream_with_context
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# Set up your OpenAI API key and client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"
)
# Open Notify API endpoint for ISS location
ISS_LOCATION_ENDPOINT = "http://api.open-notify.org/iss-now.json"


@lru_cache(maxsize=1)
def get_iss_location():
    try:
        response = requests.get(ISS_LOCATION_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print("Rate limited. Retrying in 5 seconds...")
            time.sleep(5)
            return get_iss_location()
        else:
            raise


async def get_iss_location_async():
    async with aiohttp.ClientSession() as session:
        async with session.get(ISS_LOCATION_ENDPOINT) as response:
            return await response.json()


def run_async(coro):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(coro)

@app.route("/chat/completions", methods=["POST"])
def chat_completion():
    try:
        data = request.json
        messages = data.get("messages", [])

        if not messages:
            return Response("No messages provided", status=400)

        i = 0

        for message in messages:
            print("Received messages[",i,"]:", message)
            i += 1

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_iss_location",
                    "description": "Get the current location of the International Space Station (ISS)",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    },
                },
            }
        ]

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        choice = completion.choices[0]

        if choice.finish_reason == "tool_calls":
            tool_call = choice.message.tool_calls[0]
            if tool_call.function.name == "get_iss_location":
                iss_data = get_iss_location()

                messages.append(choice.message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": "get_iss_location",
                    "content": json.dumps(iss_data),
                })

                final_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                )

                return Response(final_response.choices[0].message.content, content_type="text/plain")

        return Response(choice.message.content or "No content", content_type="text/plain")

    except Exception as e:
        print(f"CHATBOT_STEP: {traceback.format_exc()}")
        return Response(str(e), content_type="text/plain", status=500)

if __name__ == "__main__":
    app.run(debug=True)