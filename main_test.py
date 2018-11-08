import os
import json
import pytest
from datetime import datetime
from typing import List

from processor import Waypoint
from main import load_json_waypoints
from utils import convert_to_datetime

WAYPOINTS_FILE = './data/waypoints.json' # input
TRIPS_FILE = './data/trips.json' # output


def test_files_exists():
    assert os.path.exists(WAYPOINTS_FILE)
    assert os.path.exists(TRIPS_FILE)


def test_convert_to_datetime():
    sample_date: datetime = datetime(2018, 8, 10, 20, 4, 22)
    assert convert_to_datetime("2018-08-10T20:04:22Z") == sample_date


def test_validate_object():
    waypoints: List[Waypoint] = load_json_waypoints(WAYPOINTS_FILE)
    assert waypoints != None and waypoints != []
    date_time: datetime = datetime(2018, 8, 10, 20, 4, 22)
    first_element: Waypoint = Waypoint(date_time, 51.54987, 12.41039)
    assert waypoints[0] == first_element


def test_time_diff():
    waypoints: List[Waypoint] = load_json_waypoints(WAYPOINTS_FILE)
    diff: float = waypoints[1].get_time_diff(waypoints[0])
    assert diff == 24
    diff = waypoints[2].get_time_diff(waypoints[0])
    assert diff == 60
    diff = waypoints[7].get_time_diff(waypoints[0])
    assert diff == 301


def test_distance():
    waypoints: List[Waypoint] = load_json_waypoints(WAYPOINTS_FILE)
    distance: float = waypoints[1].get_distance(waypoints[0])
    assert distance > 5.4 and distance < 5.6 # data taken from website http://www.cqsrg.org/tools/GCDistance/


def test_speed():
    waypoints: List[Waypoint] = load_json_waypoints(WAYPOINTS_FILE)
    speed: float = waypoints[1].get_speed(waypoints[0])
    # moved 5m in 24s
    assert speed > 0.8 and speed < 0.85

