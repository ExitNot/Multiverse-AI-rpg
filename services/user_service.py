from typing import Optional, Dict, Any
import uuid
from datetime import datetime

from db.database_factory import DatabaseFactory
from game.utils.locale import Locale

class UserService:
    def __init__(self):        
        self.db = DatabaseFactory.get_vector_database()
        self.locale = Locale()

    async def create_user(self, telegram_id: str, username: str, language_code: str) -> Dict[str, Any]:
        """
        Create a new user account
        
        Args:
            telegram_id: User's Telegram ID
            username: User's Telegram username
            language_code: User's preferred language code
            
        Returns:
            Dict containing the created user data
            
        Raises:
            ValueError: If user with given telegram_id already exists
        """
        # Check if user already exists
        existing_user = await self.get_user_by_telegram_id(telegram_id)
        if existing_user:
            raise ValueError(f"User with telegram_id {telegram_id} already exists")

        # Validate language code
        if language_code not in self.locale.supported_languages:
            language_code = "en"  # Default to English if language not supported

        user_data = {
            "account_id": str(uuid.uuid4()),
            "telegram_id": telegram_id,
            "username": username,
            "created_at": datetime.utcnow().isoformat(),
            "game_settings": {
                "language": language_code
            }
        }

        self.db.create_account(
            account_id=user_data["account_id"],
            telegram_id=telegram_id,
            settings=user_data
        )

        return user_data

    async def get_user_by_telegram_id(self, telegram_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user by Telegram ID
        
        Args:
            telegram_id: User's Telegram ID
            
        Returns:
            Dict containing user data or None if not found
        """
        return self.db.get_account_by_telegram_id(telegram_id)

    async def update_user_settings(self, account_id: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user settings
        
        Args:
            account_id: User's account ID
            settings: New settings to update
            
        Returns:
            Updated user data
            
        Raises:
            ValueError: If user not found
        """
        user = self.db.get_account_by_id(account_id)
        if not user:
            raise ValueError(f"User with account_id {account_id} not found")

        self.db.update_account_settings(account_id=account_id, settings=settings)
        return await self.get_user_by_telegram_id(user["telegram_id"])

    async def update_user_language(self, account_id: str, language_code: str) -> Dict[str, Any]:
        """
        Update user's language preference
        
        Args:
            account_id: User's account ID
            language_code: New language code
            
        Returns:
            Updated user data
            
        Raises:
            ValueError: If language is not supported
        """
        if language_code not in self.locale.supported_languages:
            raise ValueError(f"Language {language_code} is not supported")

        return await self.update_user_settings(
            account_id=account_id,
            settings={"game_settings": {"language": language_code}}
        )

    def get_localized_message(self, user: Dict[str, Any], key: str, **kwargs) -> str:
        """
        Get localized message for user
        
        Args:
            user: User data dictionary
            key: Localization key
            **kwargs: Format arguments
            
        Returns:
            Localized message
        """
        language = user.get('game_settings', {}).get('language', 'en')
        self.locale.set_language(language)
        return self.locale.format(key, **kwargs) 