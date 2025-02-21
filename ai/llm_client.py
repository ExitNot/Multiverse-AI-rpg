import requests
import json
from config import MODEL_URL, LLAMA_API_KEY

# Client for handling LLM requests to Llama
class LLMClient:

    def __init__(self):
        self.api_url = MODEL_URL
        self.headers = {
            "Authorization": f"Bearer {LLAMA_API_KEY}",
            "Content-Type": "application/json"
        }

    def generate_text(self, system_context, story_context, user_prompt):
        '''Generates text depending on user input'''
        parameters = {
            "max_new_tokens": 1000,
            "temperature": 0.01,
            "top_k": 50,
            "top_p": 0.95,
            "return_full_text": False
        }

        payload = {
            "inputs": f"System: {system_context}\n{story_context}\nUser: {user_prompt}\nAssistant:",
            "parameters": parameters
        }

        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()["generated_text"]
        else:
            return f"Error: {response.status_code}, {response.text}"
        