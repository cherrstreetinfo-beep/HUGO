"""
Event Bus for inter-component communication
"""

from typing import Callable, Any, Dict, List
import asyncio
from dataclasses import dataclass
from datetime import datetime
from app.utils.logger import logger


@dataclass
class Event:
    """
    Represents an event in the system
    """
    event_type: str
    source: str
    data: Dict[str, Any]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class EventBus:
    """
    Central event bus for HUGO system
    """
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_history: List[Event] = []
        self.is_running = False
        self.event_queue: asyncio.Queue = None
    
    async def initialize(self):
        """
        Initialize the event bus
        """
        self.event_queue = asyncio.Queue()
        self.is_running = True
        logger.info("Event bus initialized")
    
    async def shutdown(self):
        """
        Shutdown the event bus
        """
        self.is_running = False
        logger.info("Event bus shutdown")
    
    def subscribe(self, event_type: str, callback: Callable):
        """
        Subscribe to an event type
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to event: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """
        Unsubscribe from an event type
        """
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)
            logger.debug(f"Unsubscribed from event: {event_type}")
    
    async def emit(self, event: Event):
        """
        Emit an event
        """
        if not self.is_running:
            logger.warning("Event bus is not running")
            return
        
        self.event_history.append(event)
        logger.debug(f"Event emitted: {event.event_type} from {event.source}")
        
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(event)
                    else:
                        callback(event)
                except Exception as e:
                    logger.error(f"Error in event callback: {e}", exc_info=True)
    
    def get_history(self, event_type: str = None, limit: int = 100) -> List[Event]:
        """
        Get event history
        """
        if event_type:
            return [e for e in self.event_history if e.event_type == event_type][-limit:]
        return self.event_history[-limit:]


# Global event bus instance
event_bus = EventBus()
