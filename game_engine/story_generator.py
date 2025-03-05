import logging
from ai.llm_client import LLMClient
from ai.promptsV2 import CONVERSATION_HEADER, DEFINITIONS, LANGUAGE_PROMPT, STORY_TELLER, WORLD_PROMPT, STORY_STRUCT_PROMPT
from config import dynamic_config
import json


class StoryGenerator:
    def __init__(self):
        self.client = LLMClient()
        self.logger = logging.getLogger(__name__)

    # def generate_missions_list(self): 
    # TODO have to generate short list of 3 missions with description of worlds

    def generate_story(self, context, user_input):
        response = self.client.generate_text(
            WORLD_PROMPT + "\n" + DEFINITIONS + "\n" + STORY_TELLER + "\n" + LANGUAGE_PROMPT.format(lang=dynamic_config['GAME_LANGUAGE']),
            CONVERSATION_HEADER + str(context),
            user_input)
        return response

    def generate_adventure_struct(self, topic = None):
        story_context = ""
        # if topic != None:
        #     story_context = STORY_STRUCT_PROMPT + "{mission} have to rely on " + topic + " topic"
        # else:
        #     story_context = STORY_STRUCT_PROMPT
        # response = self.client.generate_text(WORLD_PROMPT + "\n" + DEFINITIONS, STORY_STRUCT_PROMPT, "", "json_object")
        # Use for testing if do not whant to waste tokens
        response = self.client.generate_mocked_story()
        self.logger.info(response)
        return json.loads(response)