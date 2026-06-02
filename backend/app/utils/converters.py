"""
Type conversion utilities
"""

from typing import Any, Optional
import json


def to_dict(obj: Any) -> dict:
    """
    Convert object to dictionary
    """
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    if isinstance(obj, dict):
        return obj
    try:
        return json.loads(json.dumps(obj, default=str))
    except:
        return {"value": str(obj)}


def to_json_string(obj: Any) -> str:
    """
    Convert object to JSON string
    """
    return json.dumps(obj, default=str, indent=2)


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert to integer
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert to float
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
