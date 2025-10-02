"""
Qdrant Memory Manager for MCP Memory Server (Refactored Router).

This is now a lightweight router that delegates to specialized memory modules
while maintaining backward compatibility with the existing MCP server interface.
Refactored from monolithic 1,106-line class for better maintainability.
"""

import hashlib
import logging
import uuid
from datetime import datetime
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer
from src.config import Config

from .error_handler import (
    retry_embedding_operation,
    retry_qdrant_operation,
)
from .generic_memory_service import GenericMemoryService

# Import specialized memory modules
from .memory import (
    AgentRegistry,
    CollectionManager,
    EmbeddingService,
    FileMetadataManager,
    VectorOperations,
)

logger = logging.getLogger(__name__)


class QdrantMemoryManager:
    """
    Lightweight router that delegates to specialized memory modules.

    Maintains backward compatibility with existing MCP server interface
    while using modular architecture for better maintainability.
    """

    def __init__(self) -> None:
        """Initialize the Memory Manager Router."""
        # Legacy interface compatibility
        self.client: QdrantClient | None = None
        self.embedding_model: SentenceTransformer | None = None
        self.collections_initialized = False
        self.current_agent_id = None
        self.current_context = {}

        # Generic memory service for backward compatibility
        self.generic_service = GenericMemoryService()

        # Specialized modules (initialized after client setup)
        self.embedding_service: EmbeddingService | None = None
        self.collection_manager: CollectionManager | None = None
        self.vector_operations: VectorOperations | None = None
        self.agent_registry: AgentRegistry | None = None
        self.file_metadata_manager: FileMetadataManager | None = None

        # Initialize synchronously for MCP server compatibility
        self._sync_initialize()

    def _agent_id_to_point_id(self, agent_id: str) -> str:
        """Convert agent ID to valid Qdrant point ID.

        Qdrant requires point IDs to be either unsigned integers or UUIDs.
        This function converts any agent ID to a valid UUID using UUID5
        (deterministic namespace-based UUID).

        Args:
            agent_id: The original agent ID (may have prefixes like 'admin-')

        Returns:
            A valid UUID string that can be used as Qdrant point ID
        """
        # If agent_id is already a valid UUID, use it directly
        try:
            uuid.UUID(agent_id)
            return agent_id  # It's already a valid UUID
        except ValueError:
            pass

        # Create a deterministic UUID5 based on the agent_id
        # Using a fixed namespace for consistency
        namespace = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
        return str(uuid.uuid5(namespace, agent_id))

    @retry_qdrant_operation(max_attempts=3)
    def _sync_initialize(self) -> None:
        """Synchronous initialization for compatibility."""
        try:
            # Initialize the generic memory service synchronously
            import asyncio

            # Check if we can run async operations
            try:
                asyncio.get_running_loop()
                logger.warning(
                    "Already in event loop during sync initialization - " "using fallback sync init"
                )
                # Fall back to old sync initialization
                self._fallback_sync_init()
            except RuntimeError:
                # No event loop, run async initialization
                asyncio.run(self._async_initialize_generic_service())

                # Initialize legacy compatibility attributes
                self.client = self.generic_service.client
                self.embedding_model = self.generic_service.embedding_model
                self.collections_initialized = self.generic_service.initialized

            logger.info("✅ QdrantMemoryManager initialized with GenericMemoryService")

        except Exception as e:
            logger.error(f"❌ Failed to initialize QdrantMemoryManager: {e}")
            # Fall back to sync initialization
            try:
                self._fallback_sync_init()
                logger.info("✅ Fallback sync initialization completed")
            except Exception as fallback_error:
                logger.error(f"❌ Fallback initialization also failed: {fallback_error}")
                raise

    async def _async_initialize_generic_service(self) -> None:
        """Initialize the generic memory service asynchronously."""
        await self.generic_service.initialize()

    def _fallback_sync_init(self) -> None:
        """Fallback to traditional sync initialization with modular services."""
        # Initialize Qdrant client directly
        if Config.QDRANT_API_KEY:
            self.client = QdrantClient(
                host=Config.QDRANT_HOST,
                port=Config.QDRANT_PORT,
                api_key=Config.QDRANT_API_KEY,
                timeout=60,
            )
        else:
            self.client = QdrantClient(host=Config.QDRANT_HOST, port=Config.QDRANT_PORT, timeout=60)

        # Test connection
        collections = self.client.get_collections()
        logger.info(f"✅ Connected to Qdrant at {Config.QDRANT_HOST}:" f"{Config.QDRANT_PORT}")
        logger.info(f"Found {len(collections.collections)} existing collections")

        # Initialize embedding model
        from sentence_transformers import SentenceTransformer

        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        logger.info(f"✅ Loaded embedding model: {Config.EMBEDDING_MODEL}")

        # Initialize specialized modules
        self._initialize_modules()

        # Initialize collections using collection manager
        if self.collection_manager:
            self.collection_manager.sync_initialize_collections()
            self.collections_initialized = True

        # Initialize the generic service with the same client and model
        self.generic_service.client = self.client
        self.generic_service.embedding_model = self.embedding_model
        self.generic_service.initialized = True

        # Initialize collection manager for generic service (legacy)
        from .collection_manager import CollectionManager

        self.generic_service.collection_manager = CollectionManager(
            qdrant_client=self.client, embedding_dimension=Config.EMBEDDING_DIMENSION
        )

    def _initialize_modules(self) -> None:
        """Initialize specialized memory modules."""
        try:
            # Initialize embedding service
            self.embedding_service = EmbeddingService()
            # Set embedding model directly (sync initialization)
            self.embedding_service.embedding_model = self.embedding_model

            # Initialize collection manager
            self.collection_manager = CollectionManager(self.client)

            # Initialize vector operations
            self.vector_operations = VectorOperations(self.client, self.embedding_service)

            # Initialize agent registry
            self.agent_registry = AgentRegistry(self.client, self.embedding_service)

            # Initialize file metadata manager
            self.file_metadata_manager = FileMetadataManager(self.client, self.embedding_service)

            logger.info("✅ Specialized memory modules initialized")

        except Exception as e:
            logger.error(f"❌ Failed to initialize modules: {e}")
            raise

    def _ensure_legacy_collections(self) -> None:
        """Ensure legacy collections exist with backward compatibility."""
        try:
            # Skip migration for now to avoid async issues
            # Migration will be handled later when we can properly
            # manage async contexts
            logger.info("Legacy collections check completed (migration deferred)")

        except Exception as e:
            logger.error(f"❌ Failed to ensure legacy collections: {e}")
            # Don't raise - continue with degraded functionality

    @retry_qdrant_operation(max_attempts=3)
    def _sync_initialize_collections(self) -> None:
        """Initialize required collections synchronously."""
        try:
            collections_to_create = [
                Config.GLOBAL_MEMORY_COLLECTION,
                Config.LEARNED_MEMORY_COLLECTION,
                Config.FILE_METADATA_COLLECTION,
                Config.AGENT_REGISTRY_COLLECTION,
                Config.POLICY_MEMORY_COLLECTION,
                Config.POLICY_VIOLATIONS_COLLECTION,
            ]

            existing_collections = {col.name for col in self.client.get_collections().collections}

            for collection_name in collections_to_create:
                if collection_name not in existing_collections:
                    self.client.create_collection(
                        collection_name=collection_name,
                        vectors_config=VectorParams(
                            size=Config.EMBEDDING_DIMENSION, distance=Distance.COSINE
                        ),
                    )
                    logger.info(f"✅ Created collection: {collection_name}")
                else:
                    logger.info(f"📁 Collection already exists: {collection_name}")

            self.collections_initialized = True
            logger.info("✅ All collections initialized")

        except Exception as e:
            logger.error(f"❌ Failed to initialize collections: {e}")
            raise

    # MCP Server Interface Methods
    def set_agent_context(self, agent_id: str, context_type: str, description: str) -> None:
        """Set the current agent context for memory operations."""
        self.current_agent_id = agent_id
        self.current_context = {
            "agent_id": agent_id,
            "context_type": context_type,
            "description": description,
            "timestamp": datetime.now().isoformat(),
        }
        logger.info(f"🎯 Set agent context: {agent_id} ({context_type})")

    def add_to_global_memory(
        self, content: str, category: str = "general", importance: float = 0.5
    ) -> dict[str, Any]:
        """Add content to global memory via GenericMemoryService."""
        return self.generic_service.add_to_global_memory(content, category, importance)

    def add_to_learned_memory(
        self, content: str, pattern_type: str = "insight", confidence: float = 0.7
    ) -> dict[str, Any]:
        """Add learned patterns to memory via GenericMemoryService."""
        return self.generic_service.add_to_learned_memory(content, pattern_type, confidence)

    def add_to_agent_memory(
        self, content: str, agent_id: str | None = None, memory_type: str = "general"
    ) -> dict[str, Any]:
        """Add content to agent-specific memory via vector operations."""
        try:
            target_agent_id = agent_id or self.current_agent_id
            if not target_agent_id:
                return {"success": False, "error": "No agent ID provided or set in context"}

            # Ensure agent collection exists via collection manager
            if self.collection_manager:
                self.collection_manager.ensure_agent_collection(target_agent_id)

            # Use vector operations to add content
            collection_name = Config.get_collection_name("agent", target_agent_id)
            if self.vector_operations:
                result = self.vector_operations.async_add_to_memory(
                    content=content,
                    collection=collection_name,
                    metadata={"agent_id": target_agent_id, "memory_type": memory_type},
                )

                if result["success"]:
                    result["message"] = f"Added to agent memory for {target_agent_id}"

                return result
            else:
                return {"success": False, "error": "Vector operations not initialized"}

        except Exception as e:
            logger.error(f"❌ Failed to add to agent memory: {e}")
            return {"success": False, "error": str(e)}

    def query_memory(
        self, query: str, memory_types: list[str] = None, limit: int = 10, min_score: float = 0.3
    ) -> dict[str, Any]:
        """Query memory for relevant content via GenericMemoryService."""
        return self.generic_service.query_memory(query, memory_types, limit, min_score)

    def compare_against_learned_memory(
        self, situation: str, comparison_type: str = "pattern_match", limit: int = 5
    ) -> dict[str, Any]:
        """Compare situation against learned patterns via service."""
        return self.generic_service.compare_against_learned_memory(
            situation, comparison_type, limit
        )

    async def initialize(self) -> None:
        """Initialize Qdrant client and embedding model."""
        try:
            # Initialize Qdrant client
            if Config.QDRANT_API_KEY:
                self.client = QdrantClient(
                    host=Config.QDRANT_HOST,
                    port=Config.QDRANT_PORT,
                    api_key=Config.QDRANT_API_KEY,
                    timeout=60,
                )
            else:
                self.client = QdrantClient(
                    host=Config.QDRANT_HOST, port=Config.QDRANT_PORT, timeout=60
                )

            # Test connection
            collections = self.client.get_collections()
            logger.info(f"✅ Connected to Qdrant at {Config.QDRANT_HOST}:{Config.QDRANT_PORT}")
            logger.info(f"Found {len(collections.collections)} existing collections")

            # Initialize embedding model
            self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
            logger.info(f"✅ Loaded embedding model: {Config.EMBEDDING_MODEL}")

            # Initialize collections
            await self._initialize_collections()

        except Exception as e:
            logger.error(f"❌ Failed to initialize Qdrant: {e}")
            raise

    async def _initialize_collections(self) -> None:
        """Initialize required collections in Qdrant."""
        try:
            collections_to_create = [
                Config.GLOBAL_MEMORY_COLLECTION,
                Config.LEARNED_MEMORY_COLLECTION,
                Config.FILE_METADATA_COLLECTION,
                Config.AGENT_REGISTRY_COLLECTION,
            ]

            existing_collections = {col.name for col in self.client.get_collections().collections}

            for collection_name in collections_to_create:
                if collection_name not in existing_collections:
                    self.client.create_collection(
                        collection_name=collection_name,
                        vectors_config=VectorParams(
                            size=Config.EMBEDDING_DIMENSION, distance=Distance.COSINE
                        ),
                    )
                    logger.info(f"✅ Created collection: {collection_name}")
                else:
                    logger.info(f"📁 Collection already exists: {collection_name}")

            self.collections_initialized = True
            logger.info("✅ All collections initialized")

        except Exception as e:
            logger.error(f"❌ Failed to initialize collections: {e}")
            raise

    def _ensure_agent_collection(self, agent_id: str) -> None:
        """Ensure agent-specific collection exists."""
        if not self.client:
            raise RuntimeError("Qdrant client not initialized")

        collection_name = Config.get_collection_name("agent", agent_id)

        try:
            # Check if collection exists
            existing_collections = {col.name for col in self.client.get_collections().collections}

            if collection_name not in existing_collections:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=Config.EMBEDDING_DIMENSION, distance=Distance.COSINE
                    ),
                )
                logger.info(f"✅ Created agent collection: {collection_name}")

        except Exception as e:
            logger.error(f"❌ Failed to create agent collection {collection_name}: {e}")
            raise

    def _generate_content_hash(self, content: str) -> str:
        """Generate a hash for content to use as point ID."""
        # Convert hash to UUID format
        hash_hex = hashlib.sha256(content.encode("utf-8")).hexdigest()
        # Convert to UUID by taking first 32 chars and formatting as UUID
        uuid_str = (
            f"{hash_hex[:8]}-{hash_hex[8:12]}-{hash_hex[12:16]}-{hash_hex[16:20]}-{hash_hex[20:32]}"
        )
        return uuid_str

    @retry_embedding_operation(max_attempts=2)
    def _embed_text(self, text: str) -> list[float]:
        """Generate embedding for text."""
        if not self.embedding_model:
            raise RuntimeError("Embedding model not initialized")

        embedding = self.embedding_model.encode(text)
        return embedding.tolist()

    def async_add_to_memory(
        self,
        content: str,
        memory_type: str,
        agent_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Add content to specified memory type."""
        if not self.client or not self.embedding_model:
            raise RuntimeError("Memory manager not properly initialized")

        try:
            # Determine collection name
            if memory_type == "agent" and agent_id:
                self._ensure_agent_collection(agent_id)
                collection_name = Config.get_collection_name("agent", agent_id)
            else:
                collection_name = Config.get_collection_name(memory_type)

            # Generate embedding and hash
            embedding = self._embed_text(content)
            content_hash = self._generate_content_hash(content)

            # Prepare metadata
            point_metadata = {
                "content": content,
                "memory_type": memory_type,
                "content_hash": content_hash,
                "timestamp": datetime.now().isoformat(),
                **(metadata or {}),
            }

            if agent_id:
                point_metadata["agent_id"] = agent_id

            # Create point
            point = PointStruct(id=content_hash, vector=embedding, payload=point_metadata)

            # Upsert point to collection
            self.client.upsert(collection_name=collection_name, points=[point])

            logger.info(f"✅ Added content to {collection_name} (hash: {content_hash[:8]}...)")
            return content_hash

        except Exception as e:
            logger.error(f"❌ Failed to add content to memory: {e}")
            raise

    def async_query_memory(
        self,
        query: str,
        memory_type: str = "all",
        agent_id: str | None = None,
        max_results: int = 10,
    ) -> list[dict[str, Any]]:
        """Query memory collections for relevant content."""
        if not self.client or not self.embedding_model:
            raise RuntimeError("Memory manager not properly initialized")

        try:
            query_embedding = self._embed_text(query)
            results = []

            # Determine which collections to search
            collections_to_search = []

            if memory_type == "all":
                collections_to_search = [
                    Config.GLOBAL_MEMORY_COLLECTION,
                    Config.LEARNED_MEMORY_COLLECTION,
                ]
                # Add current agent's collection if available
                if agent_id:
                    agent_collection = Config.get_collection_name("agent", agent_id)
                    existing_collections = {
                        col.name for col in self.client.get_collections().collections
                    }
                    if agent_collection in existing_collections:
                        collections_to_search.append(agent_collection)
            elif memory_type == "agent" and agent_id:
                agent_collection = Config.get_collection_name("agent", agent_id)
                existing_collections = {
                    col.name for col in self.client.get_collections().collections
                }
                if agent_collection in existing_collections:
                    collections_to_search.append(agent_collection)
            else:
                collections_to_search.append(Config.get_collection_name(memory_type))

            # Search each collection
            for collection_name in collections_to_search:
                try:
                    search_results = self.client.search(
                        collection_name=collection_name,
                        query_vector=query_embedding,
                        limit=max_results,
                        score_threshold=0.1,  # Lower threshold for more results
                    )

                    for result in search_results:
                        results.append(
                            {
                                "content": result.payload.get("content", ""),
                                "score": result.score,
                                "metadata": result.payload,
                                "collection": collection_name,
                            }
                        )

                except Exception as e:
                    logger.warning(f"⚠️ Failed to search collection {collection_name}: {e}")
                    continue

            # Sort by score and limit results
            results.sort(key=lambda x: x["score"], reverse=True)
            results = results[:max_results]

            logger.info(
                f"🔍 Found {len(results)} results for query in {len(collections_to_search)} collections"
            )
            return results

        except Exception as e:
            logger.error(f"❌ Failed to query memory: {e}")
            raise

    def async_check_duplicate_with_similarity(
        self,
        content: str,
        memory_type: str,
        agent_id: str | None = None,
        threshold: float | None = None,
        enable_near_miss: bool = True,
    ) -> dict[str, Any]:
        """
        Enhanced duplicate detection using cosine similarity.

        Args:
            content: Text content to check for duplicates
            memory_type: Type of memory to check ("global", "learned", "agent")
            agent_id: Agent ID for agent-specific memory
            threshold: Similarity threshold (defaults to config value)
            enable_near_miss: Whether to detect and log near-misses

        Returns:
            Dict containing duplicate detection results and diagnostics
        """
        if not self.client or not self.embedding_model:
            raise RuntimeError("Memory manager not properly initialized")

        try:
            # Use configured thresholds
            duplicate_threshold = threshold or DEDUPLICATION_SIMILARITY_THRESHOLD
            near_miss_threshold = DEDUPLICATION_NEAR_MISS_THRESHOLD

            # Determine collection name
            if memory_type == "agent" and agent_id:
                collection_name = Config.get_collection_name("agent", agent_id)
                # Check if collection exists
                existing_collections = {
                    col.name for col in self.client.get_collections().collections
                }
                if collection_name not in existing_collections:
                    return {
                        "is_duplicate": False,
                        "is_near_miss": False,
                        "similarity_score": 0.0,
                        "reason": "Collection does not exist",
                    }
            else:
                collection_name = Config.get_collection_name(memory_type)

            # Generate embedding for comparison
            content_embedding = self._embed_text(content)

            # Search for similar content
            search_results = self.client.search(
                collection_name=collection_name,
                query_vector=content_embedding,
                limit=3,  # Get top 3 matches for diagnostics
                score_threshold=0.5,  # Lower threshold to catch near-misses
            )

            if not search_results:
                return {
                    "is_duplicate": False,
                    "is_near_miss": False,
                    "similarity_score": 0.0,
                    "reason": "No similar content found",
                }

            # Analyze the best match
            best_match = search_results[0]
            similarity_score = best_match.score

            is_duplicate = similarity_score >= duplicate_threshold
            is_near_miss = (
                enable_near_miss and not is_duplicate and similarity_score >= near_miss_threshold
            )

            # Prepare result
            result = {
                "is_duplicate": is_duplicate,
                "is_near_miss": is_near_miss,
                "similarity_score": similarity_score,
                "matched_content_hash": best_match.id,
                "matched_content": best_match.payload.get("content", "")[:100],
                "collection": collection_name,
            }

            # Add diagnostics if enabled
            if DEDUPLICATION_DIAGNOSTICS_ENABLED:
                result["diagnostics"] = {
                    "duplicate_threshold": duplicate_threshold,
                    "near_miss_threshold": near_miss_threshold,
                    "total_matches": len(search_results),
                    "top_similarities": [
                        {"score": r.score, "content_preview": r.payload.get("content", "")[:50]}
                        for r in search_results[:3]
                    ],
                }

            # Log results if enabled
            if DEDUPLICATION_LOGGING_ENABLED:
                if is_duplicate:
                    logger.info(
                        f"🔍 DUPLICATE detected in {collection_name} "
                        f"(similarity: {similarity_score:.3f} >= {duplicate_threshold})"
                    )
                elif is_near_miss:
                    logger.info(
                        f"⚠️ NEAR-MISS detected in {collection_name} "
                        f"(similarity: {similarity_score:.3f}, threshold: "
                        f"{near_miss_threshold}-{duplicate_threshold})"
                    )
                else:
                    logger.debug(
                        f"✅ No duplicate in {collection_name} "
                        f"(best similarity: {similarity_score:.3f})"
                    )

            return result

        except Exception as e:
            logger.error(f"❌ Failed to check for duplicates: {e}")
            return {
                "is_duplicate": False,
                "is_near_miss": False,
                "similarity_score": 0.0,
                "error": str(e),
            }

    def async_check_duplicate(
        self,
        content: str,
        memory_type: str,
        agent_id: str | None = None,
        threshold: float | None = None,
    ) -> bool:
        """
        Legacy duplicate detection method - maintains backward compatibility.

        This method provides the same interface as before but uses the enhanced
        cosine similarity detection under the hood.
        """
        try:
            result = self.async_check_duplicate_with_similarity(
                content=content,
                memory_type=memory_type,
                agent_id=agent_id,
                threshold=threshold,
                enable_near_miss=False,
            )
            return result.get("is_duplicate", False)
        except Exception as e:
            logger.error(f"❌ Failed to check for duplicates: {e}")
            return False

    def add_file_metadata(
        self, file_path: str, file_hash: str, chunk_ids: list[str], processing_info: dict[str, Any]
    ) -> bool:
        """Add file metadata to track processing history."""
        if not self.client:
            raise RuntimeError("Qdrant client not initialized")

        try:
            # Create metadata record
            metadata = {
                "file_path": file_path,
                "file_hash": file_hash,
                "chunk_ids": chunk_ids,
                "chunk_count": len(chunk_ids),
                "processed_timestamp": datetime.now().isoformat(),
                **processing_info,
            }

            # Use file hash as ID for deduplication
            point = PointStruct(
                id=file_hash,
                vector=[0.0] * Config.EMBEDDING_DIMENSION,  # Dummy vector
                payload=metadata,
            )

            self.client.upsert(collection_name=Config.FILE_METADATA_COLLECTION, points=[point])

            logger.info(f"📄 Added file metadata: {file_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to add file metadata: {e}")
            return False

    def get_file_metadata(self, file_path: str) -> dict[str, Any] | None:
        """Get metadata for a specific file."""
        if not self.client:
            raise RuntimeError("Qdrant client not initialized")

        try:
            # Search by file path
            search_results = self.client.scroll(
                collection_name=Config.FILE_METADATA_COLLECTION,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="file_path", match=models.MatchValue(value=file_path)
                        )
                    ]
                ),
                limit=1,
            )

            if search_results[0]:  # [0] is points, [1] is next_page_offset
                return search_results[0][0].payload
            return None

        except Exception as e:
            logger.error(f"❌ Failed to get file metadata: {e}")
            return None

    def check_file_processed(self, file_path: str, file_hash: str) -> bool:
        """Check if file has been processed with current content."""
        metadata = self.get_file_metadata(file_path)
        if metadata:
            return metadata.get("file_hash") == file_hash
        return False

    def async_delete_content(
        self, content_hash: str, memory_type: str, agent_id: str | None = None
    ) -> bool:
        """Delete content from memory by hash."""
        if not self.client:
            raise RuntimeError("Qdrant client not initialized")

        try:
            # Determine collection name
            if memory_type == "agent" and agent_id:
                collection_name = Config.get_collection_name("agent", agent_id)
            else:
                collection_name = Config.get_collection_name(memory_type)

            # Delete point
            self.client.delete(
                collection_name=collection_name,
                points_selector=models.PointIdsList(points=[content_hash]),
            )

            logger.info(f"🗑️ Deleted content from {collection_name} (hash: {content_hash[:8]}...)")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to delete content: {e}")
            return False

    def async_get_collection_info(
        self, memory_type: str, agent_id: str | None = None
    ) -> dict[str, Any]:
        """Get information about a specific collection."""
        if not self.client:
            raise RuntimeError("Qdrant client not initialized")

        try:
            # Determine collection name
            if memory_type == "agent" and agent_id:
                collection_name = Config.get_collection_name("agent", agent_id)
            else:
                collection_name = Config.get_collection_name(memory_type)

            # Get collection info
            info = self.client.get_collection(collection_name)

            return {
                "name": collection_name,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "status": info.status.value if info.status else "unknown",
            }

        except Exception as e:
            logger.error(f"❌ Failed to get collection info: {e}")
            return {"error": str(e)}

    async def cleanup(self) -> None:
        """Cleanup resources."""
        try:
            if self.client:
                # Close client connection if needed
                logger.info("🧹 Cleaning up Qdrant connections")

            if self.embedding_model:
                # Clear embedding model from memory
                self.embedding_model = None
                logger.info("🧹 Cleaned up embedding model")

        except Exception as e:
            logger.error(f"⚠️ Error during cleanup: {e}")

    # Agent Registry Management Methods

    async def register_agent(
        self,
        agent_id: str,
        agent_role: str = "general",
        memory_layers: list[str] = None,
        permissions: dict[str, Any] = None,
    ) -> dict[str, Any]:
        """Register a new agent in the agent registry."""
        try:
            if memory_layers is None:
                memory_layers = ["global", "learned"]

            if permissions is None:
                permissions = {
                    "can_read": memory_layers,
                    "can_write": memory_layers,
                    "can_admin": [],
                }

            agent_metadata = {
                "agent_id": agent_id,
                "agent_role": agent_role,
                "memory_layers": memory_layers,
                "permissions": permissions,
                "created_at": datetime.now().isoformat(),
                "status": "active",
            }

            # Create embedding for searchability
            search_text = f"Agent {agent_id} role {agent_role}"
            embedding = self.embedding_model.encode(search_text).tolist()

            # Store in agent registry
            point = PointStruct(
                id=self._agent_id_to_point_id(agent_id), vector=embedding, payload=agent_metadata
            )

            self.client.upsert(collection_name=Config.AGENT_REGISTRY_COLLECTION, points=[point])

            logger.info(f"✅ Registered agent {agent_id} with role {agent_role}")
            return {
                "success": True,
                "agent_id": agent_id,
                "message": f"Agent {agent_id} registered successfully",
            }

        except Exception as e:
            logger.error(f"❌ Failed to register agent {agent_id}: {e}")
            return {"success": False, "error": f"Failed to register agent: {str(e)}"}

    async def get_agent(self, agent_id: str) -> dict[str, Any]:
        """Get agent information from registry."""
        try:
            result = self.client.retrieve(
                collection_name=Config.AGENT_REGISTRY_COLLECTION,
                ids=[self._agent_id_to_point_id(agent_id)],
            )

            if result:
                agent_data = result[0].payload
                return {"success": True, "agent": agent_data}
            else:
                return {"success": False, "error": f"Agent {agent_id} not found"}

        except Exception as e:
            logger.error(f"❌ Failed to get agent {agent_id}: {e}")
            return {"success": False, "error": f"Failed to get agent: {str(e)}"}

    async def update_agent_permissions(
        self, agent_id: str, permissions: dict[str, Any]
    ) -> dict[str, Any]:
        """Update agent permissions."""
        try:
            # Get current agent data
            current_result = await self.get_agent(agent_id)
            if not current_result["success"]:
                return current_result

            # Update permissions
            agent_data = current_result["agent"]
            agent_data["permissions"] = permissions
            agent_data["updated_at"] = datetime.now().isoformat()

            # Create embedding for updated data
            search_text = f"Agent {agent_id} role {agent_data['agent_role']}"
            embedding = self.embedding_model.encode(search_text).tolist()

            # Update in registry
            point = PointStruct(
                id=self._agent_id_to_point_id(agent_id), vector=embedding, payload=agent_data
            )

            self.client.upsert(collection_name=Config.AGENT_REGISTRY_COLLECTION, points=[point])

            logger.info(f"✅ Updated permissions for agent {agent_id}")
            return {
                "success": True,
                "agent_id": agent_id,
                "message": "Permissions updated successfully",
            }

        except Exception as e:
            logger.error(f"❌ Failed to update agent permissions: {e}")
            return {"success": False, "error": f"Failed to update permissions: {str(e)}"}

    async def list_agents(self) -> dict[str, Any]:
        """List all registered agents."""
        try:
            # Get all points from agent registry
            result = self.client.scroll(
                collection_name=Config.AGENT_REGISTRY_COLLECTION,
                limit=100,  # Adjust as needed
                with_payload=True,
            )

            agents = []
            if result[0]:  # result is a tuple (points, next_page_offset)
                for point in result[0]:
                    agents.append(point.payload)

            return {"success": True, "agents": agents, "count": len(agents)}

        except Exception as e:
            logger.error(f"❌ Failed to list agents: {e}")
            return {"success": False, "error": f"Failed to list agents: {str(e)}"}

    async def check_agent_permission(self, agent_id: str, action: str, memory_type: str) -> bool:
        """Check if agent has permission for a specific action."""
        try:
            agent_result = await self.get_agent(agent_id)
            if not agent_result["success"]:
                return False

            permissions = agent_result["agent"].get("permissions", {})
            allowed_layers = permissions.get(f"can_{action}", [])

            return memory_type in allowed_layers

        except Exception as e:
            logger.error(f"❌ Permission check failed for {agent_id}: {e}")
            return False

    async def log_agent_action(
        self,
        agent_id: str,
        action: str,
        context: dict[str, Any],
        outcome: str,
        store_as_learned: bool = False,
    ) -> dict[str, Any]:
        """Log an agent action and optionally store as learned memory."""
        try:
            action_log = {
                "agent_id": agent_id,
                "action": action,
                "context": context,
                "outcome": outcome,
                "timestamp": datetime.now().isoformat(),
            }

            # Store as learned memory if requested
            if store_as_learned:
                learned_content = (
                    f"Agent {agent_id} performed {action}. "
                    f"Context: {context}. Outcome: {outcome}"
                )

                await self.store_memory(
                    content=learned_content,
                    collection=Config.LEARNED_MEMORY_COLLECTION,
                    metadata={
                        "type": "agent_action",
                        "pattern_type": "behavioral",
                        "agent_id": agent_id,
                        "action": action,
                        **action_log,
                    },
                )

            logger.info(f"📝 Logged action for agent {agent_id}: {action}")
            return {
                "success": True,
                "message": "Action logged successfully",
                "stored_as_learned": store_as_learned,
            }

        except Exception as e:
            logger.error(f"❌ Failed to log action for {agent_id}: {e}")
            return {"success": False, "error": f"Failed to log action: {str(e)}"}
