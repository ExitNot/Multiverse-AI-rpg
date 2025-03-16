from game.game_engine.game_engine import GameEngine
import game.config as config
import logging as log
import argparse

from game.utils.locale import Locale
    
def parse_lang(input: str) -> str:
    lang = ''
    match input.lower():
        case 'en': lang = 'en'
        case 'uk' | 'ua' | 'ukr': lang = 'uk'
        case 'cs' | 'cz': lang = 'cz'
        case 'ru': lang = 'ru'
        case _: 
            log.error("No such language found")
            'en'
    config.dynamic_config['GAME_LANGUAGE'] = lang
    log.info("Language chosen: " + lang)

def main():
    parser = argparse.ArgumentParser(description="Set the logging level via command line")
    parser.add_argument('--log', default='INFO', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    parser.add_argument('--lang', default='English', help='Set the language to llm')
    args = parser.parse_args()

    log.basicConfig(
        filename='logs/game_log.log',
        encoding='utf-8',
        level=args.log.upper(),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load the desired language
    parse_lang(args.lang)
    locale = Locale()

    print(locale["welcome_message"])
    game = GameEngine()
    game.game_loop()
    print(locale["exit_message"])

if __name__ == "__main__":
    main()