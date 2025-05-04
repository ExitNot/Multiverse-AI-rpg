from clients.base_client import BaseClient
import logging as log
import config
from game.utils.locale import Locale


class ConsoleClient(BaseClient):

    def __init__(self):
        self.running = False
        self.log = log.getLogger(__name__)

    def parse_lang(self) -> str:
        '''Parse language from input'''
        user_input = input("Choose language (en, uk, ru, cs): ")
        lang = ''
        match user_input.lower():
            case 'en':
                lang = 'en'
            case 'uk' | 'ua' | 'ukr':
                lang = 'uk'
            case 'cs' | 'cz':
                lang = 'cz'
            case 'ru':
                lang = 'ru'
            case _:
                log.error("No such language found")
                lang = 'en'
        config.dynamic_config['GAME_LANGUAGE'] = lang
        log.info("Language chosen: " + lang)
        return lang

    def start(self) -> None:
        """Start the console client"""
        self.running = True
        self.log.info("Starting console client")

        # Load the desired language
        lang = self.parse_lang()
        locale = Locale(lang)

        print(locale["welcome_message"])

        while self.running:
            try:
                user_input = input("> ")
                if user_input.lower() in ['exit', 'quit']:
                    self.stop()
                else:
                    print(f"Echo: {user_input}")
            except KeyboardInterrupt:
                self.stop()

    def stop(self) -> None:
        """Stop the console client"""
        self.running = False
        log.info("Stopping console client")
