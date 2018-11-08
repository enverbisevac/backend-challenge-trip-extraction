"""
Classes:
    - TestWaypointMethods
"""

import unittest
import json
from datetime import datetime
from typing import List

from processor import Waypoint, TripListGenerator, ListProcessor
from main import load_json_waypoints
from settings import WAYPOINTS_TEST_FILE, TRIPS_TEST_FILE
from utils import convert_to_datetime


class TestWaypointMethods(unittest.TestCase):
    """
    Testing methods for Waypoint class
    """

    def setUp(self):
        self.waypoints: List[Waypoint] = load_json_waypoints(WAYPOINTS_TEST_FILE)

    def tearDown(self):
        self.waypoints[:] = []

    def test_validate_object(self):
        """
        check deserialized object
        """
        date_time: datetime = datetime(2018, 8, 10, 20, 4, 22)
        first_element: Waypoint = Waypoint(date_time, 51.54987, 12.41039)
        assert self.waypoints[0] == first_element


    def test_time_diff(self):
        """
        check time difference between waypoints in seconds
        """
        diff: float = self.waypoints[1].get_time_diff(self.waypoints[0])
        assert diff == 24
        diff = self.waypoints[2].get_time_diff(self.waypoints[0])
        assert diff == 60
        diff = self.waypoints[7].get_time_diff(self.waypoints[0])
        assert diff == 301


    def test_distance(self):
        """
        test distance between two points, output is from
        website http://www.cqsrg.org/tools/GCDistance/
        """
        distance: float = self.waypoints[1].get_distance(self.waypoints[0])
        assert 5.4 < distance < 5.6


    def test_speed(self):
        """
        result taken from
        https://www.calculatorsoup.com/calculators/math/speed-distance-time-calculator.php
        """
        speed: float = self.waypoints[1].get_speed(self.waypoints[0])
        # moved 5m in 24s
        assert 0.8 < speed < 0.85


class TestTripListGenerator(unittest.TestCase):
    """
    Test
    """

    def setUp(self):
        waypoints: List[Waypoint] = load_json_waypoints(WAYPOINTS_TEST_FILE)
        self.generator: ListProcessor = TripListGenerator(waypoints)

    def test_generator(self):
        assert self.generator.get_trips() == []
