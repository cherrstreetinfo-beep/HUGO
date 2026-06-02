"""
General utility helper functions
"""

from typing import List, Any, Optional
from datetime import datetime, timedelta
import uuid


def generate_id() -> str:
    """
    Generate unique ID
    """
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format
    """
    return datetime.now().isoformat()


def parse_timestamp(ts: str) -> Optional[datetime]:
    """
    Parse ISO format timestamp
    """
    try:
        return datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return None


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    """
    Flatten nested dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def merge_dicts(*dicts) -> dict:
    """
    Merge multiple dictionaries
    """
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result
