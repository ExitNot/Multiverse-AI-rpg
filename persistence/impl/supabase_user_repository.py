from typing import Optional
from supabase import create_client, Client
from domain.entities import User, UserSettings
from persistence.repositories import UserRepository

class SupabaseUserRepository(UserRepository):
    """Supabase implementation of UserRepository"""
    
    def __init__(self, supabase_url: str, supabase_key: str):
        self.client: Client = create_client(supabase_url, supabase_key)
    
    def create_user(self, user: User) -> bool:
        try:
            self.client.table('users').insert(user.to_dict()).execute()
            return True
        except Exception:
            return False
    
    def get_user(self, telegram_id: int) -> Optional[User]:
        try:
            response = self.client.table('users').select('*').eq('telegram_id', telegram_id).execute()
            if response.data:
                return User.from_dict(response.data[0])
            return None
        except Exception:
            return None
    
    def update_user(self, user: User) -> bool:
        try:
            self.client.table('users').update(user.to_dict()).eq('telegram_id', user.telegram_id).execute()
            return True
        except Exception:
            return False
    
    def create_user_settings(self, settings: UserSettings) -> bool:
        try:
            self.client.table('user_settings').insert(settings.to_dict()).execute()
            return True
        except Exception:
            return False
    
    def get_user_settings(self, telegram_id: int) -> Optional[UserSettings]:
        try:
            response = self.client.table('user_settings').select('*').eq('telegram_id', telegram_id).execute()
            if response.data:
                return UserSettings.from_dict(response.data[0])
            return None
        except Exception:
            return None
    
    def update_user_settings(self, settings: UserSettings) -> bool:
        try:
            self.client.table('user_settings').update(settings.to_dict()).eq('telegram_id', settings.telegram_id).execute()
            return True
        except Exception:
            return False 