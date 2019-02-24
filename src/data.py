"""Storage classes for sensor data"""

# pylint: disable=R0902

import threading

from sensor import Distance, Touch, FakeSensor

class SensorData:
    """Contains the sensor data from the robot."""
    front_dist_0 = None # type: Distance
    front_dist_1 = None # type: Distance
    back_ground_dist = None # type: Distance
    middle_ground_dist = None # type: Distance

    back_ground_touch = None # type: Touch
    back_lifting_normal = None # type: Touch
    back_lifting_extended_max = None # type: Touch
    back_stair_touch = None # type: Touch
    front_ground_touch = None # type: Touch
    front_stair_touch = None # type: Touch
    front_lifting_normal = None # type: Touch
    front_lifting_extended_max = None # type: Touch
    front_middle_stair_touch = None # type: Touch
    middle_ground_touch = None # type: Touch

    # front_dist_0 = Distance("front_distance_0", 0)
    # front_dist_1 = Distance("front_distance_1", 1)
    # back_ground_dist = Distance("back_ground_dist", 2)
    # middle_ground_dist = Distance("back_ground_dist", 3)

    # # Touch sensors
    # back_ground_touch = Touch("back_ground_touch", 5)
    # back_lifting_normal = Touch("back_lifting_normal", 1)
    # back_lifting_extended_max = Touch("back_lifting_extended_max", 2)
    # back_stair_touch = Touch("back_stair_touch", 3)
    # front_ground_touch = Touch("front_ground_touch", 4)
    # front_stair_touch = Touch("front_stair_touch", 0)
    # front_lifting_normal = Touch("front_lifting_normal", 6)
    # front_lifting_extended_max = Touch("front_lifting_extended_max", 7)
    # front_middle_stair_touch = Touch("front_middle_stair_touch", 8)
    # middle_ground_touch = Touch("middle_ground_touch", 9)

    @staticmethod
    def init():
        # TODO(anyone): Need to check these channels

        # Distance sensors
        SensorData.front_dist_0 = Distance("front_distance_0", 0)
        SensorData.front_dist_1 = Distance("front_distance_1", 1)
        SensorData.back_ground_dist = Distance("back_ground_dist", 2)
        SensorData.middle_ground_dist = Distance("back_ground_dist", 3)

        # Touch sensors
        SensorData.back_ground_touch = Touch("back_ground_touch", 5)
        SensorData.back_lifting_normal = Touch("back_lifting_normal", 6)
        SensorData.back_lifting_extended_max = Touch("back_lifting_extended_max", 7)
        SensorData.back_stair_touch = Touch("back_stair_touch", 8)
        SensorData.front_ground_touch = Touch("front_ground_touch", 1)
        SensorData.front_stair_touch = Touch("front_stair_touch", 0)
        SensorData.front_lifting_normal = Touch("front_lifting_normal", 4)
        SensorData.front_lifting_extended_max = Touch("front_lifting_extended_max", 2)
        SensorData.front_middle_stair_touch = Touch("front_middle_stair_touch", 3)
        SensorData.middle_ground_touch = Touch("middle_ground_touch", 9)

class FakeSensorData:
    """An mock version of SensorData, containing just fake sensors."""

    def __init__(self):
        # Distance sensors
        self.front_dist_0 = FakeSensor("front_distance_0")
        self.front_dist_1 = FakeSensor("front_distance_1")
        self.back_ground_dist = FakeSensor("back_ground_dist")
        self.middle_ground_dist = FakeSensor("back_ground_dist")

        # Touch sensors
        self.back_ground_touch = FakeSensor("back_ground_touch")
        self.back_lifting_normal = FakeSensor("back_lifting_normal")
        self.back_lifting_extended_max = FakeSensor("back_lifting_extended_max")
        self.back_stair_touch = FakeSensor("back_stair_touch")
        self.front_ground_touch = FakeSensor("front_ground_touch")
        self.front_stair_touch = FakeSensor("front_stair_touch")
        self.front_lifting_normal = FakeSensor("front_lifting_normal")
        self.front_lifting_extended_max = FakeSensor("front_lifting_extended_max")
        self.front_middle_stair_touch = FakeSensor("front_middle_stair_touch")
        self.middle_ground_touch = FakeSensor("middle_ground_touch")
