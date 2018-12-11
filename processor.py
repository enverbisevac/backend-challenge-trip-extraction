# -*- coding: utf-8 -*-
"""
Classes
    - Waypoint
    - Trip

Interfaces
    - ListProcessor
    - StreamProcessor
"""

import json
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Union, NamedTuple, Tuple, List

from geopy import distance as geopy_distance
from settings import MINIMUM_SPEED, MINIMUM_TIME, MINIMUM_DISTANCE


class Waypoint(NamedTuple):
    """
    Waypoint class holds information for single spot in array of journey
    namedtuple is used because of speed and immutability
    """
    timestamp: datetime
    lat: float
    lng: float

    def get_time_diff(self, waypoint: Union['Waypoint', None]) -> int:
        """Get time difference in seconds """
        if waypoint is None or self is waypoint:
            return 0
        return (self.timestamp - waypoint.timestamp).seconds

    def get_speed(self, waypoint: Union['Waypoint', None]) -> float:
        """Calculate speed based on previous waypoint"""
        if waypoint is None or self is waypoint:
            return 0.0
        distance_km: float = self.get_distance(waypoint) / 1000
        diff_time_h: float = self.get_time_diff(waypoint) / 3600
        if diff_time_h == 0.0:
            return 0.0
        return distance_km / diff_time_h

    def get_distance(self, waypoint: Union['Waypoint', None]) -> float:
        """Calculate distance based on previous waypoint"""
        if waypoint is None or self is waypoint:
            return 0.0
        coords_a = (self.lat, self.lng)
        coords_b = (waypoint.lat, waypoint.lng)
        return float(geopy_distance.distance(coords_a, coords_b).m)


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
    def get_trips(self) -> Tuple[Trip, ...]:
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

    def __init__(self, waypoints: Tuple[Waypoint]):
        super(TripListGenerator, self).__init__(waypoints)
        self._trips: List[Trip] = []
        if waypoints is not None:
            self.set_waypoints(waypoints)

    def set_waypoints(self, waypoints: Tuple[Waypoint]):
        """ Setter method for waypoints """
        self._waypoints = waypoints
        self._generate()

    def _generate(self, debug: bool = True):
        """
        generate trips
        """
        new_waypoints = []
        trip_distance: float = 0.0
        prev_index = 0
        speed_waypoints = []
        for i in range(1, len(self._waypoints)):
            waypoint = self._waypoints[i]
            real_distance = waypoint.get_distance(self._waypoints[prev_index])
            # remove distances lower than 15 m
            if real_distance < MINIMUM_DISTANCE:
                continue
            
            # cleaning ends
            prev_point = self._waypoints[prev_index]
            current_speed = waypoint.get_speed(prev_point)
            if current_speed <= MINIMUM_SPEED:
                if waypoint.get_time_diff(prev_point) >= MINIMUM_TIME:
                    prev_index = i
                continue
            print(i, current_speed, prev_index)

            if speed_waypoints == []:
                speed_waypoints.append(self._waypoints[prev_index])

            # cleaning jumps
            # speed + short distance
            # bearing + angle aproach
            # or using Kalman filter (filters was not mentioned in README)
            # if len(speed_waypoints) > 1:
            #     previous_speed = speed_waypoints[-1].get_speed(speed_waypoints[-2])
            #     if previous_speed > 0.0:
            #         part = (current_speed - previous_speed) * 100 / previous_speed
            #         print(current_speed, previous_speed, part)
            speed_waypoints.append(waypoint)

        prev: Union[Waypoint, None] = None
        start: Waypoint = speed_waypoints[0]
        for i in range(1, len(speed_waypoints)):
            waypoint = speed_waypoints[i]
            current_speed = waypoint.get_speed(speed_waypoints[i-1])
            distance = waypoint.get_distance(speed_waypoints[i-1])

            if (prev is not None and waypoint.get_time_diff(prev) >= MINIMUM_TIME and
                    current_speed < MINIMUM_SPEED):
                self._trips.append(Trip(start=start, end=prev, distance=round(trip_distance)))
                start = waypoint
                prev = waypoint
                trip_distance = 0.0
                continue
            trip_distance += distance
            prev = waypoint
            if debug:
                new_waypoints.append({
                    "lat": waypoint.lat,
                    "lng": waypoint.lng,
                    "timestamp": waypoint.timestamp.isoformat(),
                    "speed": current_speed,
                    "distance": distance
                })
        if prev is not None:
            self._trips.append(Trip(start=start, end=prev, distance=round(trip_distance)))
        if debug:
            with open("./data/new_waypoints.json", "w") as file_handler:
                json.dump(new_waypoints, file_handler, indent=4)

    def get_trips(self) -> Tuple[Trip, ...]:
        return tuple(self._trips)
