from sensor import Distance
from sensor import Touch

class SensorData():
    """
    Contains the sensor data from the robot
    """

    # TODO(anyone) Comment beside the sensors the channel they are using

    # Distance sensors TODO(anyone): Need to check these channels
    front_dist_0 = Distance("front_distance_0", 0)
    front_dist_1 = Distance("front_distance_1", 1)
    back_ground_dist = Distance("back_ground_dist", 2)
    middle_ground_dist = Distance("back_ground_dist", 3)

    # Touch sensors TODO(anyone): Need to check these channels
    back_ground_touch = Touch("back_ground_touch", 0)
    back_lifting_normal = Touch("back_lifting_normal", 1)
    back_lifting_extended_max = Touch("back_lifting_extended_max", 2)
    front_ground_touch = Touch("front_ground_touch", 3)
    front_stair_touch = Touch("front_stair_touch", 4)
    front_lifting_normal = Touch("front_lifting_normal", 5)
    front_lifting_extended_max = Touch("front_lifting_extended_max", 6)
    front_middle_stair_touch = Touch("front_middle_stair_touch", 7)
