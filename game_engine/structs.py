
'''Structs for LLM responces'''

from typing import List


class Challenge:
    id: str
    description: str
    def __init__(self, ch_id: str, ch_description: str):
        self.id = int(ch_id.removeprefix('ch_'))
        self.description = ch_description

    def __repr__(self) -> str:
        return f"\nChallenge (ID: {self.id}; Description: {self.description})"

class Route:
    loc_id: str
    availability: str
    def __init__(self, loc_id: str, loc_availability: str):
        self.loc_id = int(loc_id.removeprefix('loc_'))
        self.availability = loc_availability

    def __repr__(self) -> str:
        return f"\nRoute (Location id: {self.loc_id}; Availability: {self.availability})"

class Location:
    id: str
    description: str
    routes: List[Route]
    def __init__(self, loc_id: str, loc_description: str, routes: List[Route]):
        self.id = int(loc_id.removeprefix('loc_'))
        self.description = loc_description
        self.routes = routes

    def __repr__(self) -> str:
        return f"\nLocation (\nID: {self.id};\nDescription: {self.description};\nRoute: {self.routes};)"

class Npc:
    name: str
    description: str
    knowledge: str
    def __init__(self, npc_name: str, npc_description: str, npc_knowledge: str):
        self.name = npc_name
        self.description = npc_description
        self.knowledge = npc_knowledge

    def __repr__(self) -> str:
        return f"\nNPC (\nName: {self.name} ;\nDescription: {self.description};\nKnowledge: {self.knowledge};)"
    
class Story:
    title: str
    description: str
    locations: List[Location]
    challenges: List[Challenge]
    npc: List[Npc]
    def __init__(self, title: str, description: str, locations: List[Location], challenges: List[Challenge], npc: List[Npc]):
        self.title = title
        self.description = description
        self.locations = locations
        self.challenges = challenges
        self.npc = npc

    def __str__(self) -> str:
        return f"Story (\nTitle:{self.title};\nDescription: {self.description};\nChallenges: \n{self.challenges};\nLocations: \n{self.locations};\nNPC's: \n{self.npc};\n"
