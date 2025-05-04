from game.game_engine.game_engine import GameEngine
import config as config
import logging as log
import argparse

from game.utils.locale import Locale
from clients.telegram_client import TelegramClient
from clients.console_client import ConsoleClient

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

def get_client(client_type: str):
    """Get client instance based on type"""
    clients = {
        'telegram': TelegramClient,
        'console': ConsoleClient
    }
    
    client_class = clients.get(client_type.lower())
    if not client_class:
        log.error(f"Unknown client type: {client_type}")
        log.info("Defaulting to console client")
        return ConsoleClient()
    
    return client_class()

def main():
    '''Start application server.'''
    parser = argparse.ArgumentParser(description="Set the logging level via command line")
    parser.add_argument('--log', default='INFO', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    parser.add_argument('--lang', default='English', help='Set the language to llm')
    parser.add_argument('--client', default='console', help='Choose client type (console, telegram)')
    args = parser.parse_args()

    log.basicConfig(
        filename='logs/game_log.log',
        filemode='a+',
        encoding='utf-8',
        level=args.log.upper(),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load the desired language
    parse_lang(args.lang)
    locale = Locale()

    print(locale["welcome_message"])
    
    # Initialize and start the chosen client
    client = get_client(args.client)
    try:
        client.start()
    except KeyboardInterrupt:
        client.stop()
        
    print(locale["exit_message"])

if __name__ == "__main__":
    main()