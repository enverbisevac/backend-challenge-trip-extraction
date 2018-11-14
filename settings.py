"""
All configuration settings for project
"""

# test settings
WAYPOINTS_TEST_FILE = './data/waypoints.json' # input
TRIPS_TEST_FILE = './data/trips.json' # output
DEFAULT_OUTPUT_FILE = './data/output.json'

MINIMUM_TIME = 180 # seconds
MINIMUM_DISTANCE = 15
MINIMUM_SPEED = (MINIMUM_DISTANCE / 1000) / (MINIMUM_TIME / 3600)
