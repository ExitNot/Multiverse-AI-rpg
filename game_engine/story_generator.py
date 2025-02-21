
from ai.llm_client import LLMClient
from config import WORLD_PROMPT

class StoryGenerator:
    def __init__(self):
        self.client = LLMClient()

    # def generate_missions_list(self): 
    # TODO have to generate short list of 3 missions with description of worlds

    # def generate_story(self, context, user_input):
    # TODO generate story depending on context and user input

    def generate_adventure_struct(self):
        task_prompt = """You have to generate short story structure with basic description of the world (2 sentences), list of {challenges} and list of {npc}. separated in json format"""
        self.client.generate_text(WORLD_PROMPT, task_prompt, "")