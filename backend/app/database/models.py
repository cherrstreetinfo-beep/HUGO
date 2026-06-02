"""
Database Models using SQLAlchemy
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Conversation(Base):
    """Conversation model"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(String(255))
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    archived = Column(Boolean, default=False)


class Message(Base):
    """Message model"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(String(255), ForeignKey("conversations.conversation_id"))
    role = Column(String(20))  # user, assistant, system
    content = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Memory(Base):
    """Memory model"""
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True)
    memory_id = Column(String(255), unique=True)
    content = Column(Text)
    content_type = Column(String(50))
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    access_count = Column(Integer, default=0)


class Task(Base):
    """Task model"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String(255), unique=True)
    name = Column(String(255))
    description = Column(Text)
    status = Column(String(50), default="pending")
    priority = Column(Integer, default=0)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)


class AgentLog(Base):
    """Agent activity log"""
    __tablename__ = "agent_logs"
    
    id = Column(Integer, primary_key=True)
    agent_name = Column(String(255))
    action = Column(String(255))
    status = Column(String(50))
    duration_ms = Column(Integer)
    result = Column(JSON)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    """Audit log for security"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True)
    action = Column(String(255))
    user_id = Column(String(255))
    resource_type = Column(String(100))
    resource_id = Column(String(255))
    changes = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
