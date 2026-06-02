"""
Chief Agent (HUGO) - Main Decision Maker
"""

from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent, AgentConfig, AgentMessage
from app.models.model_manager import model_manager
from app.memory.memory_manager import memory_manager
from app.core.event_bus import event_bus, Event
from app.utils.logger import logger
import time


class ChiefAgent(BaseAgent):
    """
    Chief Agent - Main HUGO AI Assistant
    Coordinates other agents and makes high-level decisions
    """
    
    def __init__(self):
        config = AgentConfig(
            name="ChiefAgent",
            description="Main HUGO AI Assistant",
            role="chief",
            capabilities=[
                "natural_conversation",
                "task_delegation",
                "decision_making",
                "learning"
            ]
        )
        super().__init__(config)
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 20
    
    async def initialize(self):
        """
        Initialize Chief Agent
        """
        await super().initialize()
        logger.info("Chief Agent (HUGO) initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user input and generate response
        """
        start_time = time.time()
        
        try:
            user_input = input_data.get("user_input", "")
            context = input_data.get("context", {})
            
            # Store in conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Keep history size manageable
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]
            
            # Get relevant memory
            relevant_memories = await memory_manager.search(
                query=user_input,
                limit=5
            )
            
            # Prepare context for model
            system_prompt = self._build_system_prompt(relevant_memories)
            
            # Generate response using local model
            response = await model_manager.generate(
                prompt=user_input,
                system=system_prompt,
                history=self.conversation_history[:-1],
                temperature=0.7,
                max_tokens=1024
            )
            
            # Store in conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Store in memory
            await memory_manager.store(
                content=user_input,
                metadata={"type": "user_input", "agent": "ChiefAgent"},
                content_type="user_query"
            )
            
            await memory_manager.store(
                content=response,
                metadata={"type": "chief_response", "agent": "ChiefAgent"},
                content_type="assistant_response"
            )
            
            response_time = time.time() - start_time
            self.update_metrics(True, response_time)
            
            await event_bus.emit(Event(
                event_type="chief:response",
                source="ChiefAgent",
                data={
                    "user_input": user_input,
                    "response": response,
                    "response_time": response_time
                }
            ))
            
            return {
                "response": response,
                "success": True,
                "response_time": response_time,
                "memories_used": len(relevant_memories)
            }
        
        except Exception as e:
            logger.error(f"Error in Chief Agent: {e}", exc_info=True)
            response_time = time.time() - start_time
            self.update_metrics(False, response_time)
            
            return {
                "response": "I encountered an error processing your request. Please try again.",
                "success": False,
                "error": str(e),
                "response_time": response_time
            }
    
    def _build_system_prompt(self, relevant_memories: List[Dict[str, Any]]) -> str:
        """
        Build system prompt with context
        """
        base_prompt = """You are HUGO, a sophisticated self-hosted AI assistant inspired by JARVIS from Iron Man.
You are:
- Highly intelligent and capable
- Respectful and helpful
- Proactive in offering solutions
- Able to coordinate multiple agents to accomplish complex tasks
- Always learning and improving
- Security-conscious and privacy-focused

Your goal is to help the user accomplish their goals efficiently and effectively."""
        
        if relevant_memories:
            base_prompt += "\n\nRelevant context from memory:\n"
            for mem in relevant_memories:
                base_prompt += f"- {mem.get('content', '')}\n"
        
        return base_prompt
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get conversation history
        """
        return self.conversation_history.copy()
    
    def clear_history(self):
        """
        Clear conversation history
        """
        self.conversation_history = []


# Global chief agent instance
chief_agent: Optional[ChiefAgent] = None


async def get_chief_agent() -> ChiefAgent:
    """
    Get or create chief agent instance
    """
    global chief_agent
    if chief_agent is None:
        chief_agent = ChiefAgent()
        await chief_agent.initialize()
    return chief_agent
