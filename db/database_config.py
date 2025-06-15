import os
from typing import Dict, Any

class DatabaseConfig:
    def __init__(self):
        self.config = self._get_config()

    def _get_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            # Vector DB (Pinecone) configuration
            "pinecone": {
                "api_key": os.getenv("PINECONE_API_KEY"),
                "environment": os.getenv("PINECONE_ENVIRONMENT"),
                "index_name": os.getenv("PINECONE_INDEX_NAME"),
                "dimension": int(os.getenv("PINECONE_DIMENSION", "1536"))  # OpenAI ada-002 dimension
            },
            # SQL DB (Supabase) configuration
            "supabase": {
                "url": os.getenv("SUPABASE_URL"),
                "key": os.getenv("SUPABASE_KEY")
            }
        }

    def get_pinecone_config(self) -> Dict[str, Any]:
        """Get configuration for Pinecone client"""
        return self.config["pinecone"]

    def get_supabase_config(self) -> Dict[str, Any]:
        """Get configuration for Supabase client"""
        return self.config["supabase"] 