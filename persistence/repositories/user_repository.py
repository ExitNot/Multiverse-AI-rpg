from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import User, UserSettings

class UserRepository(ABC):
    """Repository interface for user-related operations"""
    
    @abstractmethod
    def create_user(self, user: User) -> bool:
        """Create a new user"""
        pass
    
    @abstractmethod
    def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID"""
        pass
    
    @abstractmethod
    def update_user(self, user: User) -> bool:
        """Update user information"""
        pass
    
    @abstractmethod
    def create_user_settings(self, settings: UserSettings) -> bool:
        """Create user settings"""
        pass
    
    @abstractmethod
    def get_user_settings(self, telegram_id: int) -> Optional[UserSettings]:
        """Get user settings by Telegram ID"""
        pass
    
    @abstractmethod
    def update_user_settings(self, settings: UserSettings) -> bool:
        """Update user settings"""
        pass 