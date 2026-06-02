"""
Tool registry for extending agent capabilities
"""

from typing import Callable, Dict, Any, List
from app.utils.logger import logger


class Tool:
    """
    Represents a tool that agents can use
    """
    
    def __init__(self, name: str, description: str, func: Callable, parameters: Dict[str, Any]):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters
    
    async def execute(self, **kwargs) -> Any:
        """
        Execute the tool
        """
        try:
            if asyncio.iscoroutinefunction(self.func):
                return await self.func(**kwargs)
            else:
                return self.func(**kwargs)
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {e}")
            return {"error": str(e)}


class ToolRegistry:
    """
    Registry for tools that agents can use
    """
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool):
        """
        Register a tool
        """
        self.tools[tool.name] = tool
        logger.info(f"Tool registered: {tool.name}")
    
    def unregister(self, tool_name: str):
        """
        Unregister a tool
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            logger.info(f"Tool unregistered: {tool_name}")
    
    def get_tool(self, tool_name: str) -> Tool:
        """
        Get a tool by name
        """
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools.values()
        ]
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a tool
        """
        tool = self.get_tool(tool_name)
        if not tool:
            return {"error": f"Tool not found: {tool_name}"}
        return await tool.execute(**kwargs)


import asyncio

# Global tool registry
tool_registry = ToolRegistry()
