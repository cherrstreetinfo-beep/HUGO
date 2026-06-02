"""
Base Agent Class
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
from app.utils.logger import logger
from app.core.event_bus import event_bus, Event


@dataclass
class AgentConfig:
    """
    Agent configuration
    """
    name: str
    description: str
    role: str
    capabilities: List[str] = field(default_factory=list)
    max_retries: int = 3
    timeout: int = 30
    enabled: bool = True


@dataclass
class AgentMessage:
    """
    Message passed between agents
    """
    sender: str
    recipient: str
    content: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    message_id: str = ""


class BaseAgent:
    """
    Base class for all agents
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.state = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.is_running = False
        self.performance_metrics = {
            "tasks_completed": 0,
            "errors": 0,
            "average_response_time": 0
        }
    
    async def initialize(self):
        """
        Initialize agent
        """
        logger.info(f"Initializing agent: {self.config.name}")
        self.is_running = True
        
        await event_bus.emit(Event(
            event_type="agent:initialized",
            source=self.config.name,
            data={"agent": self.config.name, "role": self.config.role}
        ))
    
    async def shutdown(self):
        """
        Shutdown agent
        """
        logger.info(f"Shutting down agent: {self.config.name}")
        self.is_running = False
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input and return output
        Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement process()")
    
    async def send_message(self, message: AgentMessage):
        """
        Send message to another agent
        """
        await event_bus.emit(Event(
            event_type=f"agent:message:{message.recipient}",
            source=self.config.name,
            data={"message": message}
        ))
    
    async def receive_message(self, timeout: Optional[int] = None) -> Optional[AgentMessage]:
        """
        Receive message from message queue
        """
        try:
            message = await asyncio.wait_for(
                self.message_queue.get(),
                timeout=timeout or self.config.timeout
            )
            return message
        except asyncio.TimeoutError:
            return None
    
    def update_metrics(self, success: bool, response_time: float):
        """
        Update performance metrics
        """
        if success:
            self.performance_metrics["tasks_completed"] += 1
        else:
            self.performance_metrics["errors"] += 1
        
        # Update average response time
        total = self.performance_metrics["tasks_completed"] + self.performance_metrics["errors"]
        if total > 0:
            self.performance_metrics["average_response_time"] = (
                (self.performance_metrics["average_response_time"] * (total - 1) + response_time) / total
            )
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get agent status
        """
        return {
            "name": self.config.name,
            "role": self.config.role,
            "enabled": self.config.enabled,
            "running": self.is_running,
            "capabilities": self.config.capabilities,
            "metrics": self.performance_metrics,
            "state": self.state
        }
