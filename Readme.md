## How to run

1. Clone repo

2. Install requirements

```sh
pip install -r requirements.txt
```

3. Start local server

```sh
py custom_llm_iss.py
```

4. Forward local port using Ngrok

```sh
ngrok http 5000
```

5. change ngrok link to new one

6. Create persona

```sh
py create_persona.py
```

7. Create conversation

```sh
py create_conversation.py
```