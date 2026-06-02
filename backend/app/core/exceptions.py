"""
Custom Exceptions
"""


class HUGOException(Exception):
    """
    Base exception for HUGO system
    """
    pass


class AgentException(HUGOException):
    """
    Exception raised by agents
    """
    pass


class MemoryException(HUGOException):
    """
    Exception raised by memory system
    """
    pass


class ModelException(HUGOException):
    """
    Exception raised by model providers
    """
    pass


class VoiceException(HUGOException):
    """
    Exception raised by voice system
    """
    pass


class AutomationException(HUGOException):
    """
    Exception raised by automation system
    """
    pass


class DatabaseException(HUGOException):
    """
    Exception raised by database operations
    """
    pass


class ValidationException(HUGOException):
    """
    Exception raised during validation
    """
    pass
