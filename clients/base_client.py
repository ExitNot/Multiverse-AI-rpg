from abc import ABC, abstractmethod

class BaseClient(ABC):
    @abstractmethod
    def start(self) -> None:
        """Start the client"""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop the client"""
        pass 