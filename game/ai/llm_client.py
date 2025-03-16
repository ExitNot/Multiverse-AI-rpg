import logging
from mistralai import Mistral
from config import MISTRAL_API_KEY, MISTRAL_MODEL_NAME

# Client for handling LLM requests to Mistral
class LLMClient:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = Mistral(api_key=MISTRAL_API_KEY)

    def generate_text(self, system_context, story_context, user_prompt, response_format = "text"):
        """Generates text depending on user input"""
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
        try:
            clint_response = self.client.chat.complete(
                model=MISTRAL_MODEL_NAME,
                messages=input_prompt,
                temperature=0.2,
                stream=False,
                response_format = {
                    "type": response_format,
                }
            )

            self.logger.debug(f"Usage: {clint_response.usage}")
            assistant_msg = clint_response.choices[0].message.content

            self.logger.debug(f"Response: {assistant_msg}")
            return assistant_msg
        except Exception as error:
            self.logger.error("Failed to get model response: " + str(error))
    
    def generate_mocked_story(self):
        return basic_response
    
        

basic_response = """{
    "title_of_mission": "The Gravitational Enigma",
    "description": "In the dimension of Chronos, a world where time flows erratically and gravity shifts unpredictably, you must find and absorb the Time Anomaly. The anomaly is a mysterious entity that exhibits strange gravitational properties, and it is said to be the key to stabilizing the chaotic timeline of Chronos.",
    "locations": [
        {
            "loc_id": "loc_1",
            "loc_description": "A bustling city square filled with holographic advertisements and citizens going about their daily lives. The air is thick with the hum of technology and the scent of exotic foods from nearby vendors.",
            "routes": [
                ["loc_2", "open"],
                ["loc_3", "ch_1"]
            ]
        },
        {
            "loc_id": "loc_2",
            "loc_description": "A dimly lit alleyway behind the city square, littered with discarded tech and flickering neon signs. The alley is a haven for shady deals and clandestine meetings.",
            "routes": [
                ["loc_1", "open"],
                ["loc_4", "ch_2"]
            ]
        },
        {
            "loc_id": "loc_3",
            "loc_description": "A grand library filled with ancient tomes and advanced holographic databases. The library is a treasure trove of knowledge, guarded by a stern librarian.",
            "routes": [
                ["loc_1", "open"],
                ["loc_5", "open"]
            ]
        },
        {
            "loc_id": "loc_4",
            "loc_description": "A hidden underground lair, accessible only through a secret entrance in the alley. The lair is filled with advanced technology and guarded by a group of rogue scientists.",
            "routes": [
                ["loc_2", "open"],
                ["loc_6", "ch_3"]
            ]
        },
        {
            "loc_id": "loc_5",
            "loc_description": "A serene garden filled with lush greenery and exotic flowers. The garden is a place of tranquility and reflection, often visited by scholars and philosophers.",
            "routes": [
                ["loc_3", "open"],
                ["loc_7", "ch_4"]
            ]
        },
        {
            "loc_id": "loc_6",
            "loc_description": "A high-tech laboratory filled with advanced equipment and experiments. The laboratory is the heart of the rogue scientists' operations, where they study the Time Anomaly.",
            "routes": [
                ["loc_4", "open"],
                ["loc_8", "ch_5"]
            ]
        },
        {
            "loc_id": "loc_7",
            "loc_description": "A mysterious cave hidden deep within the garden. The cave is said to hold ancient secrets and is guarded by a powerful entity.",
            "routes": [
                ["loc_5", "open"],
                ["loc_9", "ch_6"]
            ]
        },
        {
            "loc_id": "loc_8",
            "loc_description": "A vast observatory filled with telescopes and advanced sensors. The observatory is used to study the cosmos and the Time Anomaly.",
            "routes": [
                ["loc_6", "open"],
                ["loc_9", "ch_7"]
            ]
        },
        {
            "loc_id": "loc_9",
            "loc_description": "A hidden chamber deep within the observatory, containing the Time Anomaly. The chamber is filled with strange gravitational forces and temporal distortions.",
            "routes": [
                ["loc_7", "open"],
                ["loc_8", "open"]
            ]
        }
    ],
    "challenges": [
        {
            "challenge_id": "ch_1",
            "description": "The librarian will only grant access to the restricted section if you can solve a complex riddle about the nature of time.",
            "solution_hint": "Think about the paradoxes and contradictions in time travel."
        },
        {
            "challenge_id": "ch_2",
            "description": "You must navigate a maze of holographic illusions in the alley to find the secret entrance to the underground lair.",
            "solution_hint": "Look for patterns and inconsistencies in the holograms."
        },
        {
            "challenge_id": "ch_3",
            "description": "The rogue scientists have set up a series of security protocols that require you to hack into their systems and disable the defenses.",
            "solution_hint": "Use your knowledge of advanced technology and logic to bypass the security measures."
        },
        {
            "challenge_id": "ch_4",
            "description": "You must solve a series of philosophical puzzles posed by the garden's guardian to gain access to the mysterious cave.",
            "solution_hint": "Reflect on the nature of existence and the meaning of life."
        },
        {
            "challenge_id": "ch_5",
            "description": "The laboratory is filled with dangerous experiments that require you to use your knowledge of physics and gravity to navigate safely.",
            "solution_hint": "Think about the principles of gravity and how they can be manipulated."
        },
        {
            "challenge_id": "ch_6",
            "description": "The cave is guarded by a powerful entity that challenges you to a battle of wits and logic. You must answer a series of riddles to proceed.",
            "solution_hint": "Use your knowledge of logic and reasoning to solve the riddles."
        },
        {
            "challenge_id": "ch_7",
            "description": "The observatory requires you to solve a complex puzzle involving the alignment of celestial bodies to unlock the hidden chamber.",
            "solution_hint": "Study the stars and their movements to find the correct alignment."
        }
    ],
    "npcs": [
        {
            "npc_name": "Lorelai",
            "npc_description": "A stern librarian with a keen intellect and a dry sense of humor. She is deeply knowledgeable about the history and lore of Chronos.",
            "npc_knowledge": "She knows the location of the ancient tomes that hold information about the Time Anomaly. She will only share this information if you can solve her riddle."
        },
        {
            "npc_name": "Gideon",
            "npc_description": "A charismatic rogue scientist with a penchant for dramatic flair. He is the leader of the group studying the Time Anomaly and has a deep understanding of its properties.",
            "npc_knowledge": "He knows the secrets of the underground lair and the experiments being conducted on the Time Anomaly. He will share this information if you can prove your worth."
        },
        {
            "npc_name": "Eleanor",
            "npc_description": "A wise and enigmatic philosopher who spends her days in the garden. She is known for her deep insights into the nature of existence and time.",
            "npc_knowledge": "She knows the path to the mysterious cave and the ancient secrets it holds. She will guide you if you can answer her philosophical questions."
        },
        {
            "npc_name": "Orion",
            "npc_description": "A powerful entity that guards the cave. He is a formidable opponent with a deep understanding of logic and reasoning.",
            "npc_knowledge": "He knows the true nature of the Time Anomaly and the challenges it poses. He will share this information if you can defeat him in a battle of wits."
        },
        {
            "npc_name": "Cassio",
            "npc_description": "A brilliant astronomer who works at the observatory. He is deeply passionate about the cosmos and the mysteries it holds.",
            "npc_knowledge": "He knows the secrets of the observatory and the hidden chamber. He will share this information if you can solve his celestial puzzle."
        }
    ]
}"""