from .story_generator import StoryGenerator
import json
import logging

from .structs import Challenge, Location, Npc, Route, Story
from ..utils.locale import Locale

class GameEngine:
    '''Game engine consist of main game entities and manipulate current game state'''
    def __init__(self):
        self.story_generator = StoryGenerator()
        self.is_running = False
        self.story = None
        self.message_history = []
        self.logger = logging.getLogger(__name__)
        self.loacle = Locale()

    def start_game(self):
        '''
        Game initialization. Consist of:
         - generating of available missions
         - story structure generating
         - displaying mission information
        '''
        self.is_running = True
        print(self.loacle["mission_suggestion"])
        print('(For exit the game you have to enter "exit")\n\n\n')
        
        # TODO Generating available missions
        
        story_struct = self.story_generator.generate_adventure_struct()
        self.message_history.append("Story: " + str(story_struct))
        self.write_story(story_struct)

        print("Mission: " + self.story.title + "\n")
        print(self.story.description)


    def game_loop(self):
        '''Game loop.'''
        self.start_game()
        
        while self.is_running:
            user_input = input(f"\n{self.loacle['action_msg']} > ")
            print("+=============================+")
            self.logger.info(user_input)

            if user_input.lower() == 'exit':
                self.is_running = False
                break

            response = self.story_generator.generate_story(self.message_history, user_input)
            self.message_history.append("Player: " + user_input)
            print(response)

            

    def write_story(self, story_struct):
        '''Saves story structure to domain object.'''
        self.logger.info("STORY_STRUCT: " + json.dumps(story_struct))
        locations = [Location(loc['loc_id'], loc['loc_description'], [Route(route[0], route[1]) for route in loc['routes']]) for loc in story_struct['locations']]
        npc = [Npc(n['npc_name'], n['npc_description'], n['npc_knowledge']) for n in story_struct['npcs']]
        challenges = [Challenge(ch['challenge_id'], ch['description']) for ch in story_struct['challenges']]
        self.story = Story(story_struct['title_of_mission'], story_struct['description'], locations, challenges, npc)
        self.logger.info("Story saved!")
