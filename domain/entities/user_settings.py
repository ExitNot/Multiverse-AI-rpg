from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserSettings:
    """User settings entity representing user preferences"""
    telegram_id: int
    language: str
    nickname: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @classmethod
    def from_dict(cls, data: dict) -> 'UserSettings':
        """Create a UserSettings instance from a dictionary"""
        return cls(
            telegram_id=data['telegram_id'],
            language=data['language'],
            nickname=data['nickname'],
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now(),
            updated_at=datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else datetime.now()
        )

    def to_dict(self) -> dict:
        """Convert UserSettings instance to a dictionary"""
        return {
            'telegram_id': self.telegram_id,
            'language': self.language,
            'nickname': self.nickname,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 