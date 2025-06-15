from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User entity representing a Telegram user in our system"""
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    language_code: str
    created_at: datetime = datetime.now()

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create a User instance from a dictionary"""
        return cls(
            telegram_id=data['telegram_id'],
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            language_code=data['language_code'],
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        )

    def to_dict(self) -> dict:
        """Convert User instance to a dictionary"""
        return {
            'telegram_id': self.telegram_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'language_code': self.language_code,
            'created_at': self.created_at.isoformat()
        } 