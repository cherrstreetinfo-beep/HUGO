"""
Plugin system for extending HUGO
"""

from typing import Type, Dict, Any, List
from pathlib import Path
import importlib.util
from app.utils.logger import logger


class Plugin:
    """
    Base plugin class
    """
    
    name: str = "BasePlugin"
    version: str = "1.0.0"
    description: str = "Base plugin"
    
    async def initialize(self):
        """
        Initialize plugin
        """
        pass
    
    async def shutdown(self):
        """
        Shutdown plugin
        """
        pass
    
    async def on_message(self, message: str) -> str:
        """
        Handle message
        """
        return message


class PluginManager:
    """
    Manages plugins
    """
    
    def __init__(self, plugins_dir: str = "./plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins: Dict[str, Plugin] = {}
    
    async def load_plugins(self):
        """
        Load all plugins from plugins directory
        """
        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory not found: {self.plugins_dir}")
            return
        
        for plugin_path in self.plugins_dir.glob("*/plugin.py"):
            try:
                spec = importlib.util.spec_from_file_location(
                    plugin_path.parent.name,
                    plugin_path
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, "Plugin"):
                    plugin_class = module.Plugin
                    plugin = plugin_class()
                    await plugin.initialize()
                    self.plugins[plugin.name] = plugin
                    logger.info(f"Plugin loaded: {plugin.name}")
            except Exception as e:
                logger.error(f"Error loading plugin {plugin_path}: {e}")
    
    async def shutdown_all(self):
        """
        Shutdown all plugins
        """
        for plugin in self.plugins.values():
            try:
                await plugin.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down plugin: {e}")
    
    def get_plugin(self, name: str) -> Plugin:
        """
        Get plugin by name
        """
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[Dict[str, str]]:
        """
        List all loaded plugins
        """
        return [
            {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description
            }
            for plugin in self.plugins.values()
        ]


# Global plugin manager
plugin_manager = PluginManager()
