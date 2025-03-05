from game_engine.game_engine import GameEngine
import config
import logging
import argparse

def main():
    parser = argparse.ArgumentParser(description="Set the logging level via command line")
    parser.add_argument('--log', default='INFO', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    parser.add_argument('--lang', default='English', help='Set the language to llm')
    args = parser.parse_args()

    logging.basicConfig(
        filename='logs/game_log.log',
        encoding='utf-8',
        level=args.log.upper(),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    config.dynamic_config['GAME_LANGUAGE'] = args.lang
    game = GameEngine()
    game.game_loop()

if __name__ == "__main__":
    main() 