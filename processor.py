# -*- coding: utf-8 -*-
"""
Classes
    - Waypoint
    - Trip

Interfaces
    - ListProcessor
    - StreamProcessor
"""

from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Union, NamedTuple, Tuple

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
        return (self.timestamp - waypoint.timestamp).seconds

    def get_speed(self, waypoint: 'Waypoint') -> float:
        """Calculate speed based on previous waypoint"""
        if waypoint is None:
            return 0.0
        distance_km: float = self.get_distance(waypoint) / 1000
        diff_time_h: float = self.get_time_diff(waypoint) / 60 / 60
        return distance_km / diff_time_h

    def get_distance(self, waypoint: 'Waypoint') -> float:
        """Calculate distance based on previous waypoint"""
        if waypoint is None:
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
