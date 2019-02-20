from sensor import *

class SensorData:
    """
    Contains the sensor data from the robot
    """

    front_dist_0 = Distance("front_distance_0", 0)
    front_dist_1 = Distance("front_distance_1", 1)
    back_ground_dist = Distance("back_ground_dist", 2)
    middle_ground_dist = Distance("back_ground_dist", 3)

    # Touch sensors TODO(anyone): Need to check these channels
    back_ground_touch = Touch("back_ground_touch", 0)
    back_lifting_normal = Touch("back_lifting_normal", 1)
    back_lifting_extended_max = Touch("back_lifting_extended_max", 2)
    back_stair_touch = Touch("back_stair_touch", 3)
    front_ground_touch = Touch("front_ground_touch", 4)
    front_stair_touch = Touch("front_stair_touch", 5)
    front_lifting_normal = Touch("front_lifting_normal", 6)
    front_lifting_extended_max = Touch("front_lifting_extended_max", 7)
    front_middle_stair_touch = Touch("front_middle_stair_touch", 8)
    middle_ground_touch = Touch("middle_ground_touch", 9)

    def __init__(self, is_real):
        """ initialise the sensors """
        if is_real:
            # Distance sensors TODO(anyone): Need to check these channels
            SensorData.front_dist_0 = Distance("front_distance_0", 0)
            SensorData.front_dist_1 = Distance("front_distance_1", 1)
            SensorData.back_ground_dist = Distance("back_ground_dist", 2)
            SensorData.middle_ground_dist = Distance("back_ground_dist", 3)

            # Touch sensors TODO(anyone): Need to check these channels
            SensorData.back_ground_touch = Touch("back_ground_touch", 0)
            SensorData.back_lifting_normal = Touch("back_lifting_normal", 1)
            SensorData.back_lifting_extended_max = Touch("back_lifting_extended_max", 2)
            SensorData.front_ground_touch = Touch("front_ground_touch", 3)
            SensorData.front_stair_touch = Touch("front_stair_touch", 4)
            SensorData.front_lifting_normal = Touch("front_lifting_normal", 5)
            SensorData.front_lifting_extended_max = Touch("front_lifting_extended_max", 6)
            SensorData.front_middle_stair_touch = Touch("front_middle_stair_touch", 7)
        else:
            # Distance sensors TODO(anyone): Need to check these channels
            SensorData.front_dist_0 = FakeSensor("front_distance_0")
            SensorData.front_dist_1 = FakeSensor("front_distance_1")
            SensorData.back_ground_dist = FakeSensor("back_ground_dist")
            SensorData.middle_ground_dist = FakeSensor("back_ground_dist")

            # Touch sensors TODO(anyone): Need to check these channels
            SensorData.back_ground_touch = FakeSensor("back_ground_touch")
            SensorData.back_lifting_normal = FakeSensor("back_lifting_normal")
            SensorData.back_lifting_extended_max = FakeSensor("back_lifting_extended_max")
            SensorData.front_ground_touch = FakeSensor("front_ground_touch")
            SensorData.front_stair_touch = FakeSensor("front_stair_touch")
            SensorData.front_lifting_normal = FakeSensor("front_lifting_normal")
            SensorData.front_lifting_extended_max = FakeSensor("front_lifting_extended_max")
            SensorData.front_middle_stair_touch = FakeSensor("front_middle_stair_touch")
            SensorData.middle_ground_touch = FakeSensor("middle_ground_touch")
            SensorData.back_stair_touch = FakeSensor("back_stair_touch")
