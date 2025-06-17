import requests

url = "https://tavusapi.com/v2/personas"

payload = {
    "persona_name": "ISS Tracker Bot",
    "pipeline_mode": "full",
    "system_prompt": (
        "You are a helpful assistant that provides the current location of the International Space Station. Use the `get_iss_location` function to look it up."
    ),
    "layers": {
        "llm": {
            "base_url": "https://e9f3-180-245-191-222.ngrok-free.app/",
            "api_key": "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",
            "model": "llama-3.3-70b-versatile",
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "get_iss_location",
                        "description": "Returns the current geographic location of the International Space Station (ISS).",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                }
            ]
        },
        "tts": {
          "tts_engine": "cartesia",
          "tts_emotion_control": True,
        },
        "stt": {
          "stt_engine": "tavus-advanced",
          "participant_pause_sensitivity": "high",
          "participant_interrupt_sensitivity": "high",
          "smart_turn_detection": True,
        }
    }
}
headers = {
    "x-api-key": "0b5bb0d630774b4588a17f580a7c04da",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)