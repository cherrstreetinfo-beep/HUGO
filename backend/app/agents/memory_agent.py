"""
Memory Agent - Memory Management and Retrieval
"""

from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent, AgentConfig
from app.memory.memory_manager import memory_manager
from app.utils.logger import logger


class MemoryAgent(BaseAgent):
    """
    Memory Agent - Manages memory operations
    """
    
    def __init__(self):
        config = AgentConfig(
            name="MemoryAgent",
            description="Manages memory storage and retrieval",
            role="memory",
            capabilities=[
                "memory_storage",
                "memory_retrieval",
                "memory_consolidation",
                "memory_cleanup",
                "semantic_search"
            ]
        )
        super().__init__(config)
    
    async def initialize(self):
        """
        Initialize Memory Agent
        """
        await super().initialize()
        logger.info("Memory Agent initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute memory operation
        """
        try:
            operation = input_data.get("operation", "search")
            
            if operation == "search":
                return await self._search(input_data)
            elif operation == "store":
                return await self._store(input_data)
            elif operation == "recall":
                return await self._recall(input_data)
            elif operation == "consolidate":
                return await self._consolidate()
            else:
                return {"success": False, "error": f"Unknown operation: {operation}"}
        
        except Exception as e:
            logger.error(f"Error in Memory Agent: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    async def _search(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search memory
        """
        query = input_data.get("query", "")
        limit = input_data.get("limit", 10)
        
        results = await memory_manager.search(query=query, limit=limit)
        
        return {
            "success": True,
            "operation": "search",
            "query": query,
            "results": results,
            "count": len(results)
        }
    
    async def _store(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Store in memory
        """
        content = input_data.get("content", "")
        metadata = input_data.get("metadata", {})
        content_type = input_data.get("content_type", "general")
        
        result = await memory_manager.store(
            content=content,
            metadata=metadata,
            content_type=content_type
        )
        
        return {
            "success": True,
            "operation": "store",
            "stored": result
        }
    
    async def _recall(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recall memory by ID
        """
        memory_id = input_data.get("id", "")
        
        memory = await memory_manager.get(memory_id)
        
        return {
            "success": True,
            "operation": "recall",
            "memory": memory
        }
    
    async def _consolidate(self) -> Dict[str, Any]:
        """
        Consolidate memories
        """
        result = await memory_manager.consolidate()
        
        return {
            "success": True,
            "operation": "consolidate",
            "result": result
        }


# Global memory agent instance
memory_agent: Optional[MemoryAgent] = None


async def get_memory_agent() -> MemoryAgent:
    """
    Get or create memory agent instance
    """
    global memory_agent
    if memory_agent is None:
        memory_agent = MemoryAgent()
        await memory_agent.initialize()
    return memory_agent
