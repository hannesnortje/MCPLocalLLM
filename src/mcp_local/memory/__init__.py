"""
Memory management modules for the MCP Memory Server.

This package contains specialized modules that handle different aspects
of memory management, extracted from the monolithic memory_manager.py
for better maintainability and separation of concerns.
"""

try:
    from .agent_registry import AgentRegistry
    from .collection_manager import CollectionManager
    from .embedding_service import EmbeddingService
    from .file_metadata_manager import FileMetadataManager
    from .vector_operations import VectorOperations

    __all__ = [
        "VectorOperations",
        "AgentRegistry",
        "FileMetadataManager",
        "EmbeddingService",
        "CollectionManager",
    ]
except ImportError as e:
    # Handle import errors gracefully during development
    import logging

    logging.warning(f"Memory module import error: {e}")
    __all__ = []
