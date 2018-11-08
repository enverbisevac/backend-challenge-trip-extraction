"""
Utilities
"""
from datetime import datetime


def convert_to_datetime(timestamp: str) -> datetime:
    """Helper function for converting timestamp to datetime object"""
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
