from typing import Optional, List
import pinecone
from domain.entities import Message, WorldContext
from persistence.repositories import VectorRepository

class PineconeVectorRepository(VectorRepository):
    """Pinecone implementation of VectorRepository"""
    
    def __init__(self, api_key: str, environment: str, index_name: str, dimension: int):
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        self.dimension = dimension
        
        self.client = self._initialize_client()
        self.index = self._initialize_index()
        
        # Namespaces
        self.messages_namespace = "messages"
        self.world_contexts_namespace = "world_contexts"

    def _initialize_client(self):
        """Initialize Pinecone client"""
        return pinecone.init(
            api_key=self.api_key,
            environment=self.environment
        )

    def _initialize_index(self):
        """Initialize or get existing Pinecone index"""
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine"
            )
        return pinecone.Index(self.index_name)

    def add_message(self, message: Message) -> bool:
        try:
            self.index.upsert(
                vectors=[(message.message_id, message.embedding, message.to_dict())],
                namespace=self.messages_namespace
            )
            return True
        except Exception:
            return False

    def search_similar_messages(self, query_embedding: list, n_results: int = 5) -> List[Message]:
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=n_results,
                namespace=self.messages_namespace
            )
            return [Message.from_dict(match.metadata) for match in results.matches]
        except Exception:
            return []

    def get_message(self, message_id: str) -> Optional[Message]:
        try:
            result = self.index.fetch(
                ids=[message_id],
                namespace=self.messages_namespace
            )
            if message_id in result.vectors:
                return Message.from_dict(result.vectors[message_id].metadata)
            return None
        except Exception:
            return None

    def delete_message(self, message_id: str) -> bool:
        try:
            self.index.delete(
                ids=[message_id],
                namespace=self.messages_namespace
            )
            return True
        except Exception:
            return False

    def add_world_context(self, context: WorldContext) -> bool:
        try:
            self.index.upsert(
                vectors=[(context.context_id, context.embedding, context.to_dict())],
                namespace=self.world_contexts_namespace
            )
            return True
        except Exception:
            return False

    def get_world_context(self, context_id: str) -> Optional[WorldContext]:
        try:
            result = self.index.fetch(
                ids=[context_id],
                namespace=self.world_contexts_namespace
            )
            if context_id in result.vectors:
                return WorldContext.from_dict(result.vectors[context_id].metadata)
            return None
        except Exception:
            return None

    def search_world_contexts(self, query_embedding: list, n_results: int = 5) -> List[WorldContext]:
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=n_results,
                namespace=self.world_contexts_namespace
            )
            return [WorldContext.from_dict(match.metadata) for match in results.matches]
        except Exception:
            return [] 