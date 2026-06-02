"""
WebSocket support for real-time communication
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set
from app.utils.logger import logger
import json


class ConnectionManager:
    """
    Manages WebSocket connections
    """
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, client_id: str, websocket: WebSocket):
        """Register new connection"""
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = set()
        self.active_connections[client_id].add(websocket)
        logger.info(f"Client {client_id} connected")
    
    def disconnect(self, client_id: str, websocket: WebSocket):
        """Unregister connection"""
        if client_id in self.active_connections:
            self.active_connections[client_id].discard(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
        logger.info(f"Client {client_id} disconnected")
    
    async def broadcast(self, message: dict):
        """Broadcast to all connections"""
        for client_connections in self.active_connections.values():
            for connection in client_connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting message: {e}")
    
    async def send_personal(self, client_id: str, message: dict):
        """Send to specific client"""
        if client_id in self.active_connections:
            for connection in self.active_connections[client_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending personal message: {e}")
    
    async def receive_message(self, client_id: str, websocket: WebSocket):
        """Receive message from client"""
        try:
            data = await websocket.receive_text()
            return json.loads(data)
        except WebSocketDisconnect:
            self.disconnect(client_id, websocket)
            return None
        except json.JSONDecodeError:
            return None


# Global connection manager
connection_manager = ConnectionManager()
