from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any

@dataclass
class Message:
    """Message entity representing a chat message in our system"""
    message_id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    created_at: datetime = datetime.now()

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        """Create a Message instance from a dictionary"""
        return cls(
            message_id=data['message_id'],
            content=data['content'],
            embedding=data['embedding'],
            metadata=data.get('metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        )

    def to_dict(self) -> dict:
        """Convert Message instance to a dictionary"""
        return {
            'message_id': self.message_id,
            'content': self.content,
            'embedding': self.embedding,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat()
        } 