# -*- coding: utf-8 -*-
"""
This is main app module for extracting data
"""

import sys
import json
from typing import List, NamedTuple
import datetime
from processor import Waypoint, TripListGenerator, Trip
from utils import convert_to_datetime


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(MyEncoder, self).default(obj)


def load_json_waypoints(filename):
    """
    Load file and convert it to Waypoints list of objects
    """
    waypoints: List[Waypoint] = []
    with open(filename, 'r') as file_handle:
        waypoints = json.load(file_handle,
                              object_hook=lambda d: Waypoint(convert_to_datetime(
                                  d['timestamp']), d['lat'], d['lng']))
    return waypoints


if __name__ == "__main__":
    waypoints = load_json_waypoints(sys.argv[1])
    generator = TripListGenerator(waypoints)
    print(waypoints[9].get_distance(waypoints[0]))
    print(json.dumps(generator.get_trips(), indent=4, cls=MyEncoder))
