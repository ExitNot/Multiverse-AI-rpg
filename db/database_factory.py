from typing import Optional
from db.database_config import DatabaseConfig
from db.sql_database import SQLDatabase, SupabaseDatabase
from db.vector_database import VectorDatabase, PineconeDatabase

class DatabaseFactory:
    _sql_instance: Optional[SQLDatabase] = None
    _vector_instance: Optional[VectorDatabase] = None
    
    @classmethod
    def get_sql_database(cls) -> SQLDatabase:
        """Get or create SQL database instance"""
        if cls._sql_instance is None:
            config = DatabaseConfig()
            supabase_config = config.get_supabase_config()
            cls._sql_instance = SupabaseDatabase(
                supabase_url=supabase_config['url'],
                supabase_key=supabase_config['key']
            )
        return cls._sql_instance
    
    @classmethod
    def get_vector_database(cls) -> VectorDatabase:
        """Get or create Vector database instance"""
        if cls._vector_instance is None:
            config = DatabaseConfig()
            pinecone_config = config.get_pinecone_config()
            cls._vector_instance = PineconeDatabase(
                api_key=pinecone_config['api_key'],
                environment=pinecone_config['environment'],
                index_name=pinecone_config['index_name'],
                dimension=pinecone_config['dimension']
            )
        return cls._vector_instance 