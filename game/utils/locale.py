
import json
from config import dynamic_config
import logging as log


class Locale:
    _instance = None
    _lang: str = "en"

    def __new__(cls, lang: str = "en"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._lang = lang
            with open(f'locales/{lang}.json', 'r', encoding='utf-8') as file:
                cls._instance._data = json.load(file)
        return cls._instance

    def __init__(self, lang: str = "en") -> None:
        self.log = log.getLogger(__name__)
        self.log.info(f'Loaded locale: locales/{self._lang}.json')

    def __getitem__(self, key):
        return self._data[key]
