"""
Coding Agent - Code Generation and Debugging
"""

from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent, AgentConfig
from app.models.model_manager import model_manager
from app.memory.memory_manager import memory_manager
from app.utils.logger import logger


class CodingAgent(BaseAgent):
    """
    Coding Agent - Generates, debugs, and optimizes code
    """
    
    def __init__(self):
        config = AgentConfig(
            name="CodingAgent",
            description="Generates and debugs code",
            role="coder",
            capabilities=[
                "code_generation",
                "bug_fixing",
                "code_review",
                "optimization",
                "documentation"
            ]
        )
        super().__init__(config)
    
    async def initialize(self):
        """
        Initialize Coding Agent
        """
        await super().initialize()
        logger.info("Coding Agent initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate or debug code
        """
        try:
            request_type = input_data.get("type", "generate")  # generate, debug, review, optimize
            language = input_data.get("language", "python")
            description = input_data.get("description", "")
            code = input_data.get("code", "")
            
            if request_type == "generate":
                return await self._generate_code(language, description)
            elif request_type == "debug":
                return await self._debug_code(language, code, description)
            elif request_type == "review":
                return await self._review_code(language, code)
            elif request_type == "optimize":
                return await self._optimize_code(language, code)
            else:
                return {"success": False, "error": f"Unknown request type: {request_type}"}
        
        except Exception as e:
            logger.error(f"Error in Coding Agent: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    async def _generate_code(self, language: str, description: str) -> Dict[str, Any]:
        """
        Generate code based on description
        """
        prompt = f"""Generate production-ready {language} code based on the following description.
Include proper error handling, type hints, and documentation.

Description: {description}

Provide only the code without explanations."""
        
        code = await model_manager.generate(
            prompt=prompt,
            system=f"You are an expert {language} programmer. Generate clean, efficient, well-documented code.",
            temperature=0.5,
            max_tokens=2048
        )
        
        await memory_manager.store(
            content=code,
            metadata={"type": "generated_code", "language": language},
            content_type="code"
        )
        
        return {"success": True, "code": code, "language": language}
    
    async def _debug_code(self, language: str, code: str, error: str) -> Dict[str, Any]:
        """
        Debug code
        """
        prompt = f"""Debug the following {language} code and fix the issues.

Code:
{code}

Error/Issue: {error}

Provide the fixed code with explanations of changes."""
        
        result = await model_manager.generate(
            prompt=prompt,
            system=f"You are an expert {language} debugger. Identify and fix bugs.",
            temperature=0.5,
            max_tokens=2048
        )
        
        return {"success": True, "fixed_code": result, "language": language}
    
    async def _review_code(self, language: str, code: str) -> Dict[str, Any]:
        """
        Review code for quality
        """
        prompt = f"""Perform a comprehensive code review of the following {language} code.

Code:
{code}

Provide:
1. Overall quality assessment
2. Issues and concerns
3. Improvement suggestions
4. Security considerations"""
        
        review = await model_manager.generate(
            prompt=prompt,
            system=f"You are an expert {language} code reviewer.",
            temperature=0.6,
            max_tokens=2048
        )
        
        return {"success": True, "review": review, "language": language}
    
    async def _optimize_code(self, language: str, code: str) -> Dict[str, Any]:
        """
        Optimize code for performance
        """
        prompt = f"""Optimize the following {language} code for performance and efficiency.

Code:
{code}

Provide the optimized code with explanations of optimizations."""
        
        optimized = await model_manager.generate(
            prompt=prompt,
            system=f"You are an expert {language} performance optimizer.",
            temperature=0.5,
            max_tokens=2048
        )
        
        return {"success": True, "optimized_code": optimized, "language": language}


# Global coding agent instance
coding_agent: Optional[CodingAgent] = None


async def get_coding_agent() -> CodingAgent:
    """
    Get or create coding agent instance
    """
    global coding_agent
    if coding_agent is None:
        coding_agent = CodingAgent()
        await coding_agent.initialize()
    return coding_agent
