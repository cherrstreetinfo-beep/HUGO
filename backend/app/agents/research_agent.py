"""
Research Agent - Information Gathering and Analysis
"""

from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentConfig
from app.models.model_manager import model_manager
from app.memory.memory_manager import memory_manager
from app.utils.logger import logger


class ResearchAgent(BaseAgent):
    """
    Research Agent - Performs research and analysis
    """
    
    def __init__(self):
        config = AgentConfig(
            name="ResearchAgent",
            description="Gathers and analyzes information",
            role="researcher",
            capabilities=[
                "web_research",
                "document_analysis",
                "information_synthesis",
                "fact_checking"
            ]
        )
        super().__init__(config)
    
    async def initialize(self):
        """
        Initialize Research Agent
        """
        await super().initialize()
        logger.info("Research Agent initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform research on given topic
        """
        try:
            query = input_data.get("query", "")
            depth = input_data.get("depth", "medium")  # shallow, medium, deep
            
            # Search memory for existing knowledge
            existing_knowledge = await memory_manager.search(
                query=query,
                limit=10
            )
            
            # Generate research response
            prompt = f"""Conduct thorough research on the following topic and provide comprehensive insights.
            
Topic: {query}
Depth: {depth}

Provide:
1. Overview
2. Key facts and findings
3. Analysis
4. Sources and references
5. Conclusions"""
            
            research_result = await model_manager.generate(
                prompt=prompt,
                system="You are an expert researcher. Provide accurate, well-researched, and comprehensive information.",
                temperature=0.6,
                max_tokens=2048
            )
            
            # Store research result in memory
            await memory_manager.store(
                content=research_result,
                metadata={"type": "research", "query": query, "depth": depth},
                content_type="research_result"
            )
            
            return {
                "success": True,
                "research": research_result,
                "existing_knowledge": [m.get('content') for m in existing_knowledge],
                "query": query
            }
        
        except Exception as e:
            logger.error(f"Error in Research Agent: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }


# Global research agent instance
research_agent: Optional[ResearchAgent] = None


async def get_research_agent() -> ResearchAgent:
    """
    Get or create research agent instance
    """
    global research_agent
    if research_agent is None:
        research_agent = ResearchAgent()
        await research_agent.initialize()
    return research_agent
