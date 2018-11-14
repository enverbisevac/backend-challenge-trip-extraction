# -*- coding: utf-8 -*-
"""
This is main app module for extracting data
"""

import sys
import json
import datetime
from typing import List, Tuple, Dict, Union

from processor import Waypoint, ListProcessor, TripListGenerator, Trip
from utils import convert_to_datetime
from settings import DEFAULT_OUTPUT_FILE


def default(data: datetime.datetime) -> Union[str, None]:
    """Converting datetime to string using iso format
    this function is needed for json library
    """
    if isinstance(data, (datetime.date, datetime.datetime)):
        return data.isoformat()
    return None


def load_waypoints_from_json(filename):
    """
    Load file and convert it to Waypoints list of objects

    :filename: str
    """
    waypoints: List[Waypoint] = []
    with open(filename, 'r') as file_handle:
        waypoints = json.load(file_handle,
                              object_hook=lambda d: Waypoint(convert_to_datetime(
                                  d['timestamp']), d['lat'], d['lng']))
    return waypoints


def save_trips_to_json(trips: Tuple[Trip, ...], filename: Union[str, None] = None):
    """
    Saving trips to json file format

    :param trips: Tuple[Trip]
    :filename: str
    """
    if filename is None:
        filename = DEFAULT_OUTPUT_FILE
    _trips: List[Dict] = []
    for trip in trips:
        _trips.append(trip._asdict())
    with open(filename, 'w') as file_handle:
        json.dump(_trips, file_handle, indent=4, default=default)


def main(*args: str):
    """
    Main function
    """
    output: Union[str, None] = None
    total_args = len(args)
    if total_args < 2:
        print("Usage: python3 main.py <input_file>")
        sys.exit(1)
    if total_args > 2:
        output = args[2]
    waypoints = load_waypoints_from_json(args[1])
    generator: ListProcessor = TripListGenerator(waypoints)
    save_trips_to_json(generator.get_trips(), output)

if __name__ == "__main__":
    main(*sys.argv)
