# -*- coding: utf-8 -*-
"""
Classes
    - Waypoint
    - Trip

Interfaces
    - ListProcessor
    - StreamProcessor
"""

import copy
import json
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Union, NamedTuple, Tuple, List

from geopy import distance


class Waypoint(NamedTuple):
    """
    Waypoint class holds information for single spot in array of journey
    namedtuple is used because of speed and immutability
    """
    timestamp: datetime
    lat: float
    lng: float

    def get_time_diff(self, waypoint: 'Waypoint') -> int:
        """Get time difference in seconds """
        if waypoint is None or self is waypoint:
            return 0
        return (self.timestamp - waypoint.timestamp).seconds

    def get_speed(self, waypoint: 'Waypoint') -> float:
        """Calculate speed based on previous waypoint"""
        if waypoint is None or self is waypoint:
            return 0.0
        distance_km: float = self.get_distance(waypoint) / 1000
        diff_time_h: float = self.get_time_diff(waypoint) / 60 / 60
        if diff_time_h == 0.0:
            return 0.0
        return distance_km / diff_time_h

    def get_distance(self, waypoint: 'Waypoint') -> float:
        """Calculate distance based on previous waypoint"""
        if waypoint is None or self is waypoint:
            return 0.0
        coords_a = (self.lat, self.lng)
        coords_b = (waypoint.lat, waypoint.lng)
        return float(distance.distance(coords_a, coords_b).m)


class Trip(NamedTuple): # pylint: disable=too-few-public-methods
    """
    Trip class
    """
    distance: int
    start: Waypoint
    end: Waypoint


class ListProcessor(metaclass=ABCMeta): # pylint: disable=too-few-public-methods
    """
    Processing waypoints at once
    """
    def __init__(self, waypoints: Tuple[Waypoint]):
        """
        On initialization the ListProcessor receives the full list of all
        waypoints. This list is held in memory, so the ListProcessor has access
        to the whole list of waypoints at all time during the trip extraction
        process.

        :param waypoints: Tuple[Waypoint]
        """
        self._waypoints = waypoints

    @abstractmethod
    def get_trips(self) -> Tuple[Trip]:
        """
        This function returns a list of Trips, which is derived from
        the list of waypoints, passed to the instance on initialization.
        """
        pass


class StreamProcessor(metaclass=ABCMeta): # pylint: disable=too-few-public-methods
    """
    Processing waypoint as a stream chunk
    """
    @abstractmethod
    def process_waypoint(self, waypoint: Waypoint) -> Union[Waypoint, None]:
        """
        Instead of a list of Waypoints, the StreamProcessor only receives one
        Waypoint at a time. The processor does not have access to the full list
        of waypoints.
        If the stream processor recognizes a complete trip, the processor
        returns a Trip object, otherwise it returns None.

        :param waypoint: Waypoint
        """
        pass


class TripListGenerator(ListProcessor):
    """
    Extract and process information from waypoints
    """

    def _generate(self) -> Tuple[Trip]:
        """
        generate trips
        """
        new_waypoints = []
        trips: List[Trip] = []
        if self._waypoints is None or self._waypoints == ():
            return tuple(trips)

        trip_distance = 0.0
        prev_index = 0
        start = None
        filtered_waypoints = []
        for i in range(1, len(self._waypoints)):
            waypoint = self._waypoints[i]
            real_distance = waypoint.get_distance(self._waypoints[i-1])
            # remove distances lower than 15 m
            if real_distance < 15:
                continue
            filtered_waypoints.append(waypoint)

        speed_waypoints = []
        prev = None
        for waypoint in filtered_waypoints:
            # clean by speed
            current_speed = waypoint.get_speed(prev)
            if current_speed <= (15 / 1000) / (180 / 60 / 60):
                if prev is None or waypoint.get_time_diff(prev) >= 180:
                    prev = waypoint
                continue

            speed_waypoints.append(waypoint)
            

        prev = None
        start = speed_waypoints[0]
        for waypoint in speed_waypoints:
            current_speed = waypoint.get_speed(prev)
            if waypoint.get_time_diff(prev) >= 180 and current_speed < 0.3:
                trips.append(Trip(start=start, end=prev, distance=trip_distance))
                start = waypoint
                prev = waypoint
                trip_distance = 0.0
                continue
            trip_distance += waypoint.get_distance(prev)
            prev = waypoint
            new_waypoints.append({
                "lat": waypoint.lat,
                "lng": waypoint.lng,
                "timestamp": waypoint.timestamp.isoformat(),
                "speed": current_speed
            })
        trips.append(Trip(start=start, end=prev, distance=trip_distance))
        fp = open("./data/new_waypoints.json", "w")
        json.dump(new_waypoints, fp, indent=4)
        return trips

    def get_trips(self) -> Tuple[Trip]:
        return self._generate()

    def _calculate_jumped_distance(self, start: Waypoint, end: Waypoint) -> float:
        print("jumped")
        return 0.00
