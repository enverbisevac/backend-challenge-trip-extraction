# -*- coding: utf-8 -*-
"""
Testing main function checking files and loading data
Classes:
    - TestMainMethods
"""

import os
from datetime import datetime

#testing modules
import unittest

#local modules
from settings import WAYPOINTS_TEST_FILE, TRIPS_TEST_FILE
from processor import Waypoint
from main import load_json_waypoints


class TestMainMethods(unittest.TestCase):
    """test class for main methods"""

    def setUp(self):
        date_time: datetime = datetime(2018, 8, 10, 20, 4, 22)
        self.waypoint: Waypoint = Waypoint(date_time, 51.54987, 12.41039)


    def tearDown(self):
        self.waypoint = None


    def test_files_exists(self): # pylint: disable=no-self-use
        """check if files exists"""
        assert os.path.exists(WAYPOINTS_TEST_FILE)
        assert os.path.exists(TRIPS_TEST_FILE)


    def test_waypoints(self): # pylint: disable=no-self-use
        """testing loading of waypoints from json file"""
        assert load_json_waypoints(WAYPOINTS_TEST_FILE) not in (None, [])
