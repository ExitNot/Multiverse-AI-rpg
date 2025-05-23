from game.game_engine.game_engine import GameEngine
import config as config
import logging as log
import argparse

from game.utils.locale import Locale
from clients.telegram_client import TelegramClient
from clients.console_client import ConsoleClient


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

    import os
    
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    log.basicConfig(
        filename='logs/game_log.log',
        filemode='a+',
        encoding='utf-8',
        level=args.log.upper(),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Also log to console
    console_handler = log.StreamHandler()
    console_handler.setLevel(args.log.upper())
    formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    log.getLogger().addHandler(console_handler)
    
    # Initialize and start the chosen client
    client = get_client(args.client)
    try:
        client.start()
    except KeyboardInterrupt:
        client.stop()

if __name__ == "__main__":
    main()