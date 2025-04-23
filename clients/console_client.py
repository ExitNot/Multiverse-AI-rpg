from clients.base_client import BaseClient
import logging as log

class ConsoleClient(BaseClient):
    def __init__(self):
        self.running = False
        self.log = log.getLogger(__name__)
        
    def start(self) -> None:
        """Start the console client"""
        self.running = True
        self.log.info("Starting console client")
        
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