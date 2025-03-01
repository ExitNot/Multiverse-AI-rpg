from game_engine.story_generator import StoryGenerator
import json
import logging

class GameEngine:
    def __init__(self):
        self.story_generator = StoryGenerator()
        self.is_running = False
        self.story = None
        self.message_history = []
        self.logger = logging.getLogger(__name__)

    def start_game(self):
        self.is_running = True
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
        
        while self.is_running:
            user_input = input("\nWhat will you do? > ")
            print("+=============================+")
            self.logger.info(user_input)

            if user_input.lower() == 'exit':
                self.is_running = False
                print("Thank you for adventure!")
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

class Challenge:
    def __init__(self, ch_id, ch_description):
        self.id = int(ch_id.removeprefix('ch_'))
        self.description = ch_description

    def __repr__(self) -> str:
        return f"\nChallenge (ID: {self.id}; Description: {self.description})"

class Route:
    def __init__(self, loc_id, loc_availability):
        self.loc_id = int(loc_id.removeprefix('loc_'))
        self.availability = loc_availability

    def __repr__(self) -> str:
        return f"\nRoute (Location id: {self.loc_id}; Availability: {self.availability})"

class Location:
    def __init__(self, loc_id, loc_description, route):
        self.id = int(loc_id.removeprefix('loc_'))
        self.description = loc_description
        self.route = route

    def __repr__(self) -> str:
        return f"\nLocation (\nID: {self.id};\nDescription: {self.description};\nRoute: {self.route};)"

class Npc:
    def __init__(self, npc_name, npc_description, npc_knowledge):
        self.name = npc_name
        self.description = npc_description
        self.knowledge = npc_knowledge

    def __repr__(self) -> str:
        return f"\nNPC (\nName: {self.name} ;\nDescription: {self.description};\nKnowledge: {self.knowledge};)"
    
class Story:
    def __init__(self, title, description, locations, challenges, npc):
        self.title = title
        self.description = description
        self.locations = locations
        self.challenges = challenges
        self.npc = npc

    def __str__(self) -> str:
        return f"Story (\nTitle:{self.title};\nDescription: {self.description};\nChallenges: \n{self.challenges};\nLocations: \n{self.locations};\nNPC's: \n{self.npc};\n"
