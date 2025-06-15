from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities import Message, WorldContext

class VectorRepository(ABC):
    """Repository interface for vector-based operations"""
    
    @abstractmethod
    def add_message(self, message: Message) -> bool:
        """Add a new message"""
        pass
    
    @abstractmethod
    def search_similar_messages(self, query_embedding: list, n_results: int = 5) -> List[Message]:
        """Search for similar messages"""
        pass
    
    @abstractmethod
    def get_message(self, message_id: str) -> Optional[Message]:
        """Get message by ID"""
        pass
    
    @abstractmethod
    def delete_message(self, message_id: str) -> bool:
        """Delete message by ID"""
        pass
    
    @abstractmethod
    def add_world_context(self, context: WorldContext) -> bool:
        """Add a new world context"""
        pass
    
    @abstractmethod
    def get_world_context(self, context_id: str) -> Optional[WorldContext]:
        """Get world context by ID"""
        pass
    
    @abstractmethod
    def search_world_contexts(self, query_embedding: list, n_results: int = 5) -> List[WorldContext]:
        """Search for similar world contexts"""
        pass 