from game_engine.story_generator import StoryGenerator
import json
import logging

class GameEngine:
    def __init__(self):
        self.story_generator = StoryGenerator()
        self.is_running = False
        self.story_struct = ""
        self.logger = logging.getLogger(__name__)

    def start_game(self):
        self.is_running = True
        print("Hi adventurer. You ready to take your next mission?\n")
        print("(For exit the game you have to enter \"exit\")\n\n\n")
        
        # TODO Generating available missions
        
        self.story_struct = json.loads(self.story_generator.generate_adventure_struct())
        print("Mission: " + self.story_struct['title_of_mission'] + "\n")
        print(self.story_struct['description'])

    def game_loop(self):
        self.start_game()
        
        while self.is_running:
            user_input = input("\nWhat will you do? > ")
            
            if user_input.lower() == 'exit':
                self.is_running = False
                print("Thank you for adventure!")
                break
            
            # response = self.story_generator.generate_response(user_input)
            # print("\n" + response) 