"""
Utility functions
"""

from datetime import datetime
from utils import convert_to_datetime


def test_convert_to_datetime():
    """testing function convert_to_datetime"""
    sample_date: datetime = datetime(2018, 8, 10, 20, 4, 22)
    assert convert_to_datetime("2018-08-10T20:04:22Z") == sample_date
