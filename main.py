# -*- coding: utf-8 -*-
"""This is main app module for extracting data"""

import json
from typing import List
from processor import Waypoint
from utils import convert_to_datetime


def load_json_waypoints(filename):
    """Load file and convert it to Waypoints"""
    waypoints: List[Waypoint] = []
    with open(filename, 'r') as file_handle:
        waypoints = json.load(file_handle,
                              object_hook=lambda d: Waypoint(convert_to_datetime(
                                  d['timestamp']), d['lat'], d['lng']))
    return waypoints


if __name__ == "__main__":
    pass
