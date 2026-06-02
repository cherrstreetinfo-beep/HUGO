"""
Core HUGO Engine
"""

from typing import Optional, Dict, Any
from app.agents.orchestrator import AgentOrchestrator
from app.memory.memory_manager import MemoryManager
from app.models.model_manager import ModelManager
from app.voice.voice_processor import VoiceProcessor
from app.automation.task_executor import TaskExecutor
from app.core.event_bus import event_bus, Event
from app.utils.logger import logger


class HUGOEngine:
    """
    Central HUGO AI Operating System Engine
    """
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.memory_manager = MemoryManager()
        self.model_manager = ModelManager()
        self.voice_processor = VoiceProcessor()
        self.task_executor = TaskExecutor()
        self.is_initialized = False
    
    async def initialize(self):
        """
        Initialize the engine and all components
        """
        logger.info("Initializing HUGO Engine...")
        
        try:
            await self.memory_manager.initialize()
            await self.model_manager.initialize()
            await self.orchestrator.initialize()
            await self.task_executor.initialize()
            
            self.is_initialized = True
            logger.info("HUGO Engine initialized successfully")
            
            await event_bus.emit(Event(
                event_type="engine:initialized",
                source="engine",
                data={"status": "ready"}
            ))
        except Exception as e:
            logger.error(f"Error initializing HUGO Engine: {e}", exc_info=True)
            raise
    
    async def process_input(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process user input and return response
        """
        if not self.is_initialized:
            raise RuntimeError("Engine not initialized")
        
        try:
            response = await self.orchestrator.process_request(
                user_input=user_input,
                context=context or {}
            )
            return response
        except Exception as e:
            logger.error(f"Error processing input: {e}", exc_info=True)
            raise
    
    async def execute_task(self, task_name: str, parameters: Dict[str, Any]) -> Any:
        """
        Execute a task through the automation system
        """
        if not self.is_initialized:
            raise RuntimeError("Engine not initialized")
        
        return await self.task_executor.execute(task_name, parameters)
    
    async def shutdown(self):
        """
        Shutdown the engine
        """
        logger.info("Shutting down HUGO Engine...")
        
        await self.task_executor.shutdown()
        await self.orchestrator.shutdown()
        await self.model_manager.shutdown()
        await self.memory_manager.shutdown()
        
        self.is_initialized = False
        logger.info("HUGO Engine shutdown complete")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get engine status
        """
        return {
            "initialized": self.is_initialized,
            "memory_status": self.memory_manager.get_status(),
            "model_status": self.model_manager.get_status(),
            "agents_status": self.orchestrator.get_status(),
            "voice_enabled": self.voice_processor.is_enabled()
        }


# Global engine instance
engine: Optional[HUGOEngine] = None


async def get_engine() -> HUGOEngine:
    """
    Get or create the global engine instance
    """
    global engine
    if engine is None:
        engine = HUGOEngine()
        await engine.initialize()
    return engine
