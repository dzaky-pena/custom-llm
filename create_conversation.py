import requests

url = "https://tavusapi.com/v2/conversations"

payload = {
    "replica_id": "r79e1c033f",
    "persona_id": "pf74c66c8d70",
    "callback_url": "https://e9f3-180-245-191-222.ngrok-free.app/chat/completions",
    "properties": {
        "max_call_duration": 3600,
        "participant_left_timeout": 60,
        "participant_absent_timeout": 300,
    }
}
headers = {
    "x-api-key": "api-key",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)