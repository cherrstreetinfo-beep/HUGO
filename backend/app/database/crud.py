"""
Database CRUD operations
"""

from sqlalchemy.orm import Session
from app.database.models import Conversation, Message, Memory, Task, AgentLog
from datetime import datetime
from typing import Optional, List


class ConversationCRUD:
    @staticmethod
    def create(db: Session, conversation_id: str, user_id: str, title: str):
        db_conv = Conversation(
            conversation_id=conversation_id,
            user_id=user_id,
            title=title
        )
        db.add(db_conv)
        db.commit()
        return db_conv
    
    @staticmethod
    def get(db: Session, conversation_id: str):
        return db.query(Conversation).filter(
            Conversation.conversation_id == conversation_id
        ).first()
    
    @staticmethod
    def list_by_user(db: Session, user_id: str, limit: int = 50):
        return db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).limit(limit).all()


class MessageCRUD:
    @staticmethod
    def create(db: Session, conversation_id: str, role: str, content: str, metadata: dict = None):
        db_msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata=metadata or {}
        )
        db.add(db_msg)
        db.commit()
        return db_msg
    
    @staticmethod
    def get_by_conversation(db: Session, conversation_id: str, limit: int = 100):
        return db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit).all()


class MemoryCRUD:
    @staticmethod
    def create(db: Session, memory_id: str, content: str, content_type: str, metadata: dict = None):
        db_mem = Memory(
            memory_id=memory_id,
            content=content,
            content_type=content_type,
            metadata=metadata or {}
        )
        db.add(db_mem)
        db.commit()
        return db_mem
    
    @staticmethod
    def get(db: Session, memory_id: str):
        return db.query(Memory).filter(Memory.memory_id == memory_id).first()
    
    @staticmethod
    def search(db: Session, content_type: str, limit: int = 50):
        return db.query(Memory).filter(
            Memory.content_type == content_type
        ).order_by(Memory.updated_at.desc()).limit(limit).all()


class TaskCRUD:
    @staticmethod
    def create(db: Session, task_id: str, name: str, description: str = "", priority: int = 0):
        db_task = Task(
            task_id=task_id,
            name=name,
            description=description,
            priority=priority,
            status="pending"
        )
        db.add(db_task)
        db.commit()
        return db_task
    
    @staticmethod
    def get(db: Session, task_id: str):
        return db.query(Task).filter(Task.task_id == task_id).first()
    
    @staticmethod
    def list_by_status(db: Session, status: str, limit: int = 50):
        return db.query(Task).filter(
            Task.status == status
        ).order_by(Task.priority.desc()).limit(limit).all()
    
    @staticmethod
    def update_status(db: Session, task_id: str, status: str):
        db_task = db.query(Task).filter(Task.task_id == task_id).first()
        if db_task:
            db_task.status = status
            if status == "completed":
                db_task.completed_at = datetime.utcnow()
            db.commit()
        return db_task


class AgentLogCRUD:
    @staticmethod
    def create(db: Session, agent_name: str, action: str, status: str, duration_ms: int, result: dict = None, error: str = None):
        db_log = AgentLog(
            agent_name=agent_name,
            action=action,
            status=status,
            duration_ms=duration_ms,
            result=result or {},
            error_message=error
        )
        db.add(db_log)
        db.commit()
        return db_log
