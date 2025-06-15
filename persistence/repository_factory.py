from typing import Optional
from persistence.repositories import UserRepository, VectorRepository
from persistence.implementations import SupabaseUserRepository, PineconeVectorRepository
from db.database_config import DatabaseConfig

class RepositoryFactory:
    """Factory for creating repository instances"""
    
    _user_repository: Optional[UserRepository] = None
    _vector_repository: Optional[VectorRepository] = None
    
    @classmethod
    def get_user_repository(cls) -> UserRepository:
        """Get or create UserRepository instance"""
        if cls._user_repository is None:
            config = DatabaseConfig()
            supabase_config = config.get_supabase_config()
            cls._user_repository = SupabaseUserRepository(
                supabase_url=supabase_config['url'],
                supabase_key=supabase_config['key']
            )
        return cls._user_repository
    
    @classmethod
    def get_vector_repository(cls) -> VectorRepository:
        """Get or create VectorRepository instance"""
        if cls._vector_repository is None:
            config = DatabaseConfig()
            pinecone_config = config.get_pinecone_config()
            cls._vector_repository = PineconeVectorRepository(
                api_key=pinecone_config['api_key'],
                environment=pinecone_config['environment'],
                index_name=pinecone_config['index_name'],
                dimension=pinecone_config['dimension']
            )
        return cls._vector_repository 