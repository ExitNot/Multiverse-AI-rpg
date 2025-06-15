from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any

@dataclass
class WorldContext:
    """World context entity representing game world information"""
    context_id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @classmethod
    def from_dict(cls, data: dict) -> 'WorldContext':
        """Create a WorldContext instance from a dictionary"""
        return cls(
            context_id=data['context_id'],
            content=data['content'],
            embedding=data['embedding'],
            metadata=data.get('metadata', {}),
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else datetime.now()
        )

    def to_dict(self) -> dict:
        """Convert WorldContext instance to a dictionary"""
        return {
            'context_id': self.context_id,
            'content': self.content,
            'embedding': self.embedding,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 