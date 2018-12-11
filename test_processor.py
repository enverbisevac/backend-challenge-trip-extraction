from datetime import datetime, timedelta

import pytest

from processor import TripListGenerator, Waypoint, Trip


@pytest.fixture
def processor():
    return TripListGenerator


class TestProcessor:
    def test_extracts_trip_with_all_distances_gt_15m(self, processor):
        start_dt = datetime(2018, 1, 1, 0, 0, 0)
        waypoints = []
        for i in range(21):
            waypoints.append(
                Waypoint(
                    start_dt + timedelta(seconds=10*i),
                    0,
                    0.0005 * i
                )
            )
        trips = processor(waypoints).get_trips()
        assert len(trips) == 1
        trip: Trip = trips[0]
        assert 1100 <= trip.distance <= 1115
        assert trip.start == Waypoint(
            start_dt,
            0,
            0
        )
        assert trip.end == Waypoint(
            start_dt + timedelta(seconds=10*20),
            0,
            0.01
        )

    def test_extracts_trip_with_all_distances_lt_15m(self, processor):
        start_dt = datetime(2018, 1, 1, 0, 0, 0)
        waypoints = []
        for i in range(101):
            waypoints.append(
                Waypoint(
                    start_dt + timedelta(seconds=10*i),
                    0,
                    0.0001 * i
                )
            )
        trips = processor(waypoints).get_trips()
        assert len(trips) == 1
        trip: Trip = trips[0]
        assert 1100 <= trip.distance <= 1115
        assert trip.start == Waypoint(
            start_dt,
            0,
            0
        )
        assert trip.end == Waypoint(
            start_dt + timedelta(seconds=10*100),
            0,
            0.01
        )

    def test_extracts_trip_with_turn(self, processor):
        start_dt = datetime(2018, 1, 1, 0, 0, 0)
        waypoints = []
        for i in range(11):
            waypoints.append(
                Waypoint(
                    start_dt + timedelta(seconds=10 * i),
                    0,
                    0.0005 * i
                )
            )
        turn_start_dt = start_dt + timedelta(seconds=100)
        for i in range(11):
            waypoints.append(
                Waypoint(
                    turn_start_dt + timedelta(seconds=10 * i),
                    0.0005 * i,
                    0.005
                )
            )

        trips = processor(waypoints).get_trips()
        assert len(trips) == 1
        trip: Trip = trips[0]
        assert 1100 <= trip.distance <= 1115
        assert trip.start == Waypoint(
            start_dt,
            0,
            0
        )
        assert trip.end == Waypoint(
            start_dt + timedelta(seconds=10 * 20),
            0.005,
            0.005
        )
    @pytest.mark.skip("no reason")
    def test_extracts_trip_with_gps_jump(self, processor):
        start_dt = datetime(2018, 1, 1, 0, 0, 0)
        waypoints = []
        for i in range(21):
            if i == 10:
                waypoints.append(
                    Waypoint(
                        start_dt + timedelta(seconds=10 * i - 1),
                        1,
                        1
                    )
                )
            waypoints.append(
                Waypoint(
                    start_dt + timedelta(seconds=10*i),
                    0,
                    0.0005 * i
                )
            )
        trips = processor(waypoints).get_trips()
        assert len(trips) == 1
        trip: Trip = trips[0]
        assert 1100 <= trip.distance <= 1115
        assert trip.start == Waypoint(
            start_dt,
            0,
            0
        )
        assert trip.end == Waypoint(
            start_dt + timedelta(seconds=10*20),
            0,
            0.01
        )

    def test_extracts_trip_when_car_was_standing_still_and_then_moved(
            self, processor
    ):
        start_dt = datetime(2018, 1, 1, 0, 0, 0)
        waypoints = []
        for i in range(11):
            waypoints.append(
                Waypoint(
                    start_dt + timedelta(seconds=10 * i),
                    0,
                    0.0
                )
            )

        actual_start_dt = start_dt + timedelta(seconds=100)
        for i in range(21):
            waypoints.append(
                Waypoint(
                    actual_start_dt + timedelta(seconds=10*i),
                    0,
                    0.0005 * i
                )
            )
        trips = processor(waypoints).get_trips()
        assert len(trips) == 1
        trip: Trip = trips[0]
        assert 1100 <= trip.distance <= 1115
        assert trip.start == Waypoint(
            actual_start_dt,
            0,
            0
        )
        assert trip.end == Waypoint(
            actual_start_dt + timedelta(seconds=10*20),
            0,
            0.01
        )