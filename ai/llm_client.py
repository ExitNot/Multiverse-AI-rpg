import requests
import json
import logging
from mistralai import Mistral
from config import MISTRAL_API_KEY, MISTRAL_MODEL_NAME

# Client for handling LLM requests to Llama
class LLMClient:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = Mistral(api_key=MISTRAL_API_KEY)

    def generate_text(self, system_context, story_context, user_prompt):
        '''Generates text depending on user input'''
        if story_context != "": 
            system_prompt = system_context + "\n" + story_context
        else: system_prompt = system_context

        input_prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # Logging the request
        self.logger.debug(f"Sending request to LLM API with payload: {input_prompt}")

        # ======================================
        # try:
        #     clint_response = self.client.chat.complete(
        #         model=MISTRAL_MODEL_NAME,
        #         messages=input_prompt,
        #         # max_tokens=5000,
        #         temperature=0.2,
        #         stream=False,
        #         response_format = {
        #             "type": "json_object",
        #         }
        #     )
        # except:
        #     self.logger.error("Failed to get model response")
        
        # self.logger.debug(f"Usage: {clint_response.usage}")
        # assistant_msg = clint_response.choices[0].message.content
        # ======================================
        # Response Mock
        assistant_msg = '{\n  "title_of_mission": "The Shattered Chronoscope",\n  "description": "Welcome to Chrono-7, a dimension where time flows in unpredictable currents and eddies. The sky is a swirling vortex of temporal distortions, and the landscape is a patchwork of different eras and technologies. ",\n  "locations": [\n    {\n      "loc_id": "loc_1",\n      "loc_description": "The Temporal Crossroads: A bustling market where beings from various time periods trade artifacts and information. The air is thick with the scent of ozone and the hum of temporal displacement.",\n      "routes": [\n        {"loc_id": "loc_2", "loc_availability": "open"},\n        {"loc_id": "loc_3", "loc_availability": "ch_1"},\n        {"loc_id": "loc_4", "loc_availability": "hidden; Talk to the mysterious cloaked figure in the market"}\n      ]\n    },\n    {\n      "loc_id": "loc_2",\n      "loc_description": "The Crystal Caverns: Deep underground caverns filled with luminescent crystals that emit soft glows and whispers of time. The caverns are home to creatures adapted to the temporal flux.",\n      "routes": [\n        {"loc_id": "loc_1", "loc_availability": "open"},\n        {"loc_id": "loc_5", "loc_availability": "ch_2"},\n        {"loc_id": "loc_6", "loc_availability": "hidden; Solve the crystal puzzle to reveal the path"}\n      ]\n    },\n    {\n      "loc_id": "loc_3",\n      "loc_description": "The Floating Islands: Islands suspended in the sky by temporal anomalies. Each island hosts a different era, from medieval castles to futuristic cities.",\n      "routes": [\n        {"loc_id": "loc_1", "loc_availability": "open"},\n        {"loc_id": "loc_7", "loc_availability": "ch_3"},\n        {"loc_id": "loc_8", "loc_availability": "hidden; Find the time-locked chest and open it"}\n      ]\n    },\n    {\n      "loc_id": "loc_4",\n      "loc_description": "The Eternal Library: A vast library containing scrolls, books, and data crystals from all time periods. The air is filled with the soft murmur of knowledge being shared.",\n      "routes": [\n        {"loc_id": "loc_1", "loc_availability": "open"},\n        {"loc_id": "loc_9", "loc_availability": "ch_4"}\n      ]\n    },\n    {\n      "loc_id": "loc_5",\n      "loc_description": "The Temporal Vortex: A swirling maelstrom of time energy. Navigating it requires precise timing and quick reflexes.",\n      "routes": [\n        {"loc_id": "loc_2", "loc_availability": "open"},\n        {"loc_id": "loc_9", "loc_availability": "ch_5"}\n      ]\n    },\n    {\n      "loc_id": "loc_6",\n      "loc_description": "The Ancient Ruins: Crumbling structures from a forgotten civilization. The ruins hold secrets of time manipulation.",\n      "routes": [\n        {"loc_id": "loc_2", "loc_availability": "open"},\n        {"loc_id": "loc_7", "loc_availability": "ch_6"}\n      ]\n    },\n    {\n      "loc_id": "loc_7",\n      "loc_description": "The Timekeeper\'s Sanctum: A hidden sanctuary where the guardians of time reside. The sanctum is filled with temporal artifacts and guarded by powerful beings.",\n      "routes": [\n        {"loc_id": "loc_3", "loc_availability": "open"},\n        {"loc_id": "loc_6", "loc_availability": "open"},\n        {"loc_id": "loc_9", "loc_availability": "ch_7"}\n      ]\n    },\n    {\n      "loc_id": "loc_8",\n      "loc_description": "The Chronal Forge: A workshop where temporal devices are crafted and repaired. The forge is run by a skilled artisan who understands the intricacies of time.",\n      "routes": [\n        {"loc_id": "loc_3", "loc_availability": "open"},\n        {"loc_id": "loc_9", "loc_availability": "ch_8"}\n      ]\n    },\n    {\n      "loc_id": "loc_9",\n      "loc_description": "The Nexus of Eternity: The heart of the temporal flux, where the time anomaly resides. The nexus is a dangerous place, filled with unstable temporal energies.",\n      "routes": [\n        {"loc_id": "loc_4", "loc_availability": "open"},\n        {"loc_id": "loc_5", "loc_availability": "open"},\n        {"loc_id": "loc_7", "loc_availability": "open"},\n        {"loc_id": "loc_8", "loc_availability": "open"}\n      ]\n    }\n  ],\n  "challenges": [\n    {\n      "ch_id": "ch_1",\n      "ch_description": "Solve the temporal riddle posed by the market\'s gatekeeper to gain access to the Floating Islands."\n    },\n    {\n      "ch_id": "ch_2",\n      "ch_description": "Navigate the crystal maze without disturbing the temporal balance to reach the Temporal Vortex."\n    },\n    {\n      "ch_id": "ch_3",\n      "ch_description": "Defeat the temporal guardian in a battle of wits and reflexes to access the Timekeeper\'s Sanctum."\n    },\n    {\n      "ch_id": "ch_4",\n      "ch_description": "Decipher the ancient language in the library to find the hidden path to the Nexus of Eternity."\n    },\n    {\n      "ch_id": "ch_5",\n      "ch_description": "Survive the temporal storm in the vortex by solving time-based puzzles."\n    },\n    {\n      "ch_id": "ch_6",\n      "ch_description": "Assemble the broken time artifact found in the ruins to open a portal to the Timekeeper\'s Sanctum."\n    },\n    {\n      "ch_id": "ch_7",\n      "ch_description": "Convince the Timekeeper to grant you access to the Nexus of Eternity by proving your worth."\n    },\n    {\n      "ch_id": "ch_8",\n      "ch_description": "Craft a temporal key using the forge\'s tools and materials to unlock the path to the Nexus of Eternity."\n    }\n  ],\n  "npc": [\n    {\n      "npc_name": "Zephyr",\n      "npc_description": "A mysterious cloaked figure with glowing eyes, often seen in the Temporal Crossroads.",\n      "npc_knowledge": "Knows the secret path to the Floating Islands and the location of the time-locked chest."\n    },\n    {\n      "npc_name": "Lumina",\n      "npc_description": "A crystalline entity residing in the Crystal Caverns, emitting a soft glow.",\n      "npc_knowledge": "Understands the crystal puzzle and can guide you through the temporal maze."\n    },\n    {\n      "npc_name": "Chronos",\n      "npc_description": "A stern guardian with a mechanical arm, found in the Timekeeper\'s Sanctum.",\n      "npc_knowledge": "Knows the rituals and tests required to prove your worth to the Timekeeper."\n    },\n    {\n      "npc_name": "Epoch",\n      "npc_description": "An ancient scholar with a beard of flowing time energy, found in the Eternal Library.",\n      "npc_knowledge": "Can translate the ancient language and provide hints about the hidden path to the Nexus of Eternity."\n    },\n    {\n      "npc_name": "Tempus",\n      "npc_description": "A skilled artisan with temporal tools integrated into his body, found in the Chronal Forge.",\n      "npc_knowledge": "Knows how to craft the temporal key and can provide materials for it."\n    }\n  ]\n}'

        self.logger.debug(f"Response: {assistant_msg}")
        return assistant_msg
        