from game_engine.story_generator import StoryGenerator
import json
import logging
from game.config import dynamic_config

from game_engine.structs import Challenge, Location, Npc, Route, Story
from utils.locale import Locale

class GameEngine:
    def __init__(self):
        self.story_generator = StoryGenerator()
        self.is_running = False
        self.story = None
        self.message_history = []
        self.logger = logging.getLogger(__name__)

    def start_game(self):
        self.is_running = True
        self.logger.info("Language choosen:" + dynamic_config['GAME_LANGUAGE'])
        print("Hi adventurer. You ready to take your next mission?\n")
        print("(For exit the game you have to enter \"exit\")\n\n\n")
        
        # TODO Generating available missions
        
        story_struct = self.story_generator.generate_adventure_struct()
        self.message_history.append("Story: " + str(story_struct))
        self.write_story(story_struct)

        print("Mission: " + self.story.title + "\n")
        print(self.story.description)


    def game_loop(self):
        self.start_game()
        loacle = Locale()
        
        while self.is_running:
            user_input = input(f"\n{loacle["action_msg"]} > ")
            print("+=============================+")
            self.logger.info(user_input)

            if user_input.lower() == 'exit':
                self.is_running = False
                break

            response = self.story_generator.generate_story(self.message_history, user_input)
            self.message_history.append("Player: " + user_input)
            print(response)

            

    def write_story(self, story_struct):
        self.logger.info("STORY_STRUCT: " + json.dumps(story_struct))
        locations = [Location(loc['loc_id'], loc['loc_description'], [Route(route[0], route[1]) for route in loc['routes']]) for loc in story_struct['locations']]
        npc = [Npc(n['npc_name'], n['npc_description'], n['npc_knowledge']) for n in story_struct['npcs']]
        challenges = [Challenge(ch['challenge_id'], ch['description']) for ch in story_struct['challenges']]
        self.story = Story(story_struct['title_of_mission'], story_struct['description'], locations, challenges, npc)
        self.logger.info("Story saved!")
