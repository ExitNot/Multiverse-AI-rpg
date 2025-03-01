from ai.llm_client import LLMClient
from ai.prompts import WORLD_PROMPT, STORY_STRUCT_PROMPT
import json

class StoryGenerator:
    def __init__(self):
        self.client = LLMClient()

    # def generate_missions_list(self): 
    # TODO have to generate short list of 3 missions with description of worlds

    # def generate_story(self, context, user_input):
    # TODO generate story depending on context and user input

    def generate_adventure_struct(self, topic = None):
        story_context = ""
        if topic != None:
            story_context = STORY_STRUCT_PROMPT + "{mission} have to rely on " + topic + " topic"
        else:
            story_context = STORY_STRUCT_PROMPT
        response = self.client.generate_text(WORLD_PROMPT, STORY_STRUCT_PROMPT, "")
        return json.loads(response)