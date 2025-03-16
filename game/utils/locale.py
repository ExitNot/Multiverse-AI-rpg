import json
from config import dynamic_config
import logging as log

class Locale:
    _instance = None
    lang = 'en'

    def __new__(self):
        if self._instance is None:
            lang = dynamic_config['GAME_LANGUAGE']
            with open(f'locales/{lang}.json', 'r', encoding='utf-8') as file:
                self._instance = json.load(file)
        return self._instance
    
    def __init__(self) -> None:
        log.info(f'Loaded locale: locales/{self.lang}.json')