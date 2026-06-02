"""
Scheduler for recurring tasks
"""

from typing import Callable, Dict, Any
from datetime import datetime, timedelta
from app.utils.logger import logger
import asyncio


class TaskScheduler:
    """
    Simple task scheduler for recurring tasks
    """
    
    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.is_running = False
    
    async def initialize(self):
        """
        Start the scheduler
        """
        self.is_running = True
        logger.info("Task scheduler started")
        asyncio.create_task(self._run())
    
    async def shutdown(self):
        """
        Stop the scheduler
        """
        self.is_running = False
        logger.info("Task scheduler stopped")
    
    def schedule(self, task_id: str, callback: Callable, interval_seconds: int, args: tuple = ()):
        """
        Schedule a recurring task
        """
        self.tasks[task_id] = {
            "callback": callback,
            "interval": interval_seconds,
            "args": args,
            "last_run": datetime.now() - timedelta(seconds=interval_seconds),
            "enabled": True
        }
        logger.info(f"Task scheduled: {task_id} (interval: {interval_seconds}s)")
    
    def unschedule(self, task_id: str):
        """
        Remove scheduled task
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            logger.info(f"Task unscheduled: {task_id}")
    
    async def _run(self):
        """
        Main scheduler loop
        """
        while self.is_running:
            now = datetime.now()
            
            for task_id, task_info in list(self.tasks.items()):
                if not task_info["enabled"]:
                    continue
                
                if (now - task_info["last_run"]).total_seconds() >= task_info["interval"]:
                    try:
                        callback = task_info["callback"]
                        args = task_info["args"]
                        
                        if asyncio.iscoroutinefunction(callback):
                            await callback(*args)
                        else:
                            callback(*args)
                        
                        task_info["last_run"] = now
                    except Exception as e:
                        logger.error(f"Error running scheduled task {task_id}: {e}")
            
            await asyncio.sleep(1)


# Global scheduler
scheduler = TaskScheduler()
