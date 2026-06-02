"""
Planner Agent - Task Planning and Decomposition
"""

from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentConfig
from app.models.model_manager import model_manager
from app.utils.logger import logger
import json


class PlannerAgent(BaseAgent):
    """
    Planner Agent - Breaks down complex tasks into steps
    """
    
    def __init__(self):
        config = AgentConfig(
            name="PlannerAgent",
            description="Breaks down complex tasks into manageable steps",
            role="planner",
            capabilities=[
                "task_decomposition",
                "step_planning",
                "resource_allocation",
                "dependency_mapping"
            ]
        )
        super().__init__(config)
    
    async def initialize(self):
        """
        Initialize Planner Agent
        """
        await super().initialize()
        logger.info("Planner Agent initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a plan for the given task
        """
        try:
            task = input_data.get("task", "")
            context = input_data.get("context", {})
            
            prompt = f"""You are a task planning expert. Break down the following task into clear, actionable steps.
For each step, specify:
1. What needs to be done
2. Which agent should handle it (research, coding, browser, file, memory, automation, or security)
3. Dependencies on other steps
4. Estimated time
5. Required resources

Task: {task}

Respond in JSON format with a 'steps' array."""
            
            plan_text = await model_manager.generate(
                prompt=prompt,
                system="You are an expert at breaking down complex tasks into manageable steps.",
                temperature=0.5,
                max_tokens=2048
            )
            
            # Parse the plan
            plan = self._parse_plan(plan_text)
            
            return {
                "success": True,
                "plan": plan,
                "raw_response": plan_text
            }
        
        except Exception as e:
            logger.error(f"Error in Planner Agent: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_plan(self, plan_text: str) -> List[Dict[str, Any]]:
        """
        Parse plan from model response
        """
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', plan_text, re.DOTALL)
            if json_match:
                plan_data = json.loads(json_match.group())
                return plan_data.get('steps', [])
        except json.JSONDecodeError:
            pass
        
        # Fallback: parse as simple text
        return [{"description": plan_text}]


# Global planner agent instance
planner_agent: Optional[PlannerAgent] = None


async def get_planner_agent() -> PlannerAgent:
    """
    Get or create planner agent instance
    """
    global planner_agent
    if planner_agent is None:
        planner_agent = PlannerAgent()
        await planner_agent.initialize()
    return planner_agent
