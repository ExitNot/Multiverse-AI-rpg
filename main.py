from game_engine.game_engine import GameEngine
import logging
import argparse

parser = argparse.ArgumentParser(description="Set the logging level via command line")
parser.add_argument('--log', default='ERROR', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
args = parser.parse_args()

logging.basicConfig(
    level=args.log.upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    game = GameEngine()
    game.game_loop()

if __name__ == "__main__":
    main() 