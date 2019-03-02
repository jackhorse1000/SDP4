"""Storage classes for sensor data"""

# pylint: disable=R0902

from sensor import Distance, Touch, FakeSensor, TouchSensorsI2c, RotaryEncoder

class SensorData:
    """Contains the sensor data from the robot."""

    front_dist_0 = None # type: Distance
    front_dist_1 = None # type: Distance
    back_stair_dist = None # type: Distance
    back_ground_dist = None # type: Distance
    middle_ground_dist = None # type: Distance

    # back_ground_touch = None # type: Touch
    front_ground_touch = None # type: Touch
    front_stair_touch = None # type: Touch
    front_lifting_normal = None # type: Touch
    front_lifting_extended_max = None # type: Touch
    front_middle_stair_touch = None # type: Touch

    middle_ground_touch = None # type: TouchSensorsI2c
    back_stair_touch = None # type: Touch
    back_lifting_normal = None # type: Touch
    back_lifting_extended_max = None # type: Touch
    back_ground_touch = None # type: Touch

    def __init__(self) -> None:
        # TODO(anyone): Need to check these channels

        # Distance sensors
        self.front_dist_0 = Distance("front_distance_0", 0)
        self.front_dist_1 = Distance("front_distance_1", 1)
        self.back_stair_dist = Distance("back_stair_touch", 2)
        self.back_ground_dist = Distance("back_ground_dist", 3)
        self.middle_ground_dist = Distance("back_ground_dist", 4)

        # Touch sensors
        # self.back_ground_touch = Touch("back_ground_touch", 5)
        self.front_ground_touch = Touch("front_ground_touch", 5)
        self.front_stair_touch = Touch("front_stair_touch", 4)
        self.front_lifting_normal = Touch("front_lifting_normal", 1)
        self.front_lifting_extended_max = Touch("front_lifting_extended_max", 2)
        self.front_middle_stair_touch = Touch("front_middle_stair_touch", 3)

        self.middle_ground_touch = TouchSensorsI2c("middle_ground_touch")
        self.back_stair_touch = Touch("back_stair_touch", 6)
        self.back_lifting_normal = Touch("back_lifting_normal", 7)
        self.back_lifting_extended_max = Touch("back_lifting_extended_max", 0)
        self.back_ground_touch = Touch("back_ground_touch", 2) #TODO(anyone): Update channel

        self.front_lifting_rot = RotaryEncoder("front_lifting_rot")
        self.back_lifting_rot = RotaryEncoder("back_lifting_rot")

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
