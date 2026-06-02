"""
Input validation utilities
"""

from typing import Any, Optional
import re


def validate_string(value: Any, min_length: int = 1, max_length: Optional[int] = None) -> bool:
    """
    Validate string input
    """
    if not isinstance(value, str):
        return False
    if len(value) < min_length:
        return False
    if max_length and len(value) > max_length:
        return False
    return True


def validate_email(email: str) -> bool:
    """
    Validate email address
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_url(url: str) -> bool:
    """
    Validate URL
    """
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None


def validate_json_key(key: str) -> bool:
    """
    Validate JSON key format
    """
    return isinstance(key, str) and len(key) > 0 and not key.startswith('_')
