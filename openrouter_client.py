import os
from dotenv import load_dotenv
import requests

load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

class OpenRouterClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://openrouter.ai/api/v1/chat/completions'

    def ask(self, prompt, model="openai/gpt-3.5-turbo"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

if __name__ == "__main__":
    client = OpenRouterClient(OPENROUTER_API_KEY)
    reply = client.ask("Summarize this email: Hi, can we reschedule our meeting to next week?")
    print("AI Response:", reply)
