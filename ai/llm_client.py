import requests
import json
import logging
from config import MODEL_URL, HF_API_KEY

# Client for handling LLM requests to Llama
class LLMClient:

    def __init__(self):
        self.api_url = MODEL_URL
        self.headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger(__name__)

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

        # Logging the request
        self.logger.debug(f"Sending request to LLM API with payload: {payload}")

        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))

        # Logging the response
        if response.status_code == 200:
            self.logger.info("Successfully received response from LLM API")
            self.logger.debug(f"Response: {response.json()}")
            return response.json()[0]['generated_text']
        else:
            error_msg = f"Error: {response.status_code}, {response.text}"
            self.logger.error(f"Failed to get response from LLM API: {error_msg}")
            return error_msg
        