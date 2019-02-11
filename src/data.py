import scoped_lock

class SensorData():
    """
    Contains the sensor data from the robot
    """

    # TODO(anyone) Comment beside the sensors below the channel they are using
    # TODO(anyone) We will need to add lock if this is multithreaded

    # Distance sensors
    front_dist = 0.0
    back_ground_dist = 0.0

    # Touch sensors
    is_back_ground_touch = False
    is_back_lifting_normal = False
    is_back_lifting_extended_max = False

    is_front_ground_touch = False
    is_front_stair_touch = False
    is_front_lifting_normal = False
    is_front_lifting_extended_max = False # Fully extended is true when touch sensor reads 0

    is_front_middle_stair_touch = False

    @staticmethod
    def get_front_middle_stair_touch():
        """ Return the state of the front middle touch sensor for stair sensing """
        return SensorData.is_front_middle_stair_touch

    @staticmethod
    def set_front_middle_stair_touch(is_touch):
        """ Set the state of the front middle touch sensor for stair sensing """
        SensorData.is_front_middle_stair_touch = is_touch

    @staticmethod
    def get_front_lifting_extended_max():
        """ Return the state of the front lifting touch sensor for max position """
        return SensorData.is_front_lifting_extended_max

    @staticmethod
    def set_front_lifting_extended_max(is_touch):
        """ Set the state of the front lifting touch sensor for max position """
        SensorData.is_front_lifting_extended_max = is_touch

    @staticmethod
    def get_front_lifting_extended_max():
        """ Return the state of the front lifting touch sensor for max position """
        return SensorData.is_front_lifting_extended_max

    @staticmethod
    def set_front_lifting_extended_max(is_touch):
        """ Set the state of the front lifting touch sensor for max position """
        SensorData.is_front_lifting_extended_max = is_touch

    @staticmethod
    def get_front_lifting_normal():
        """ Return the state of the front lifting touch sensor for normal position """
        return SensorData.is_front_lifting_normal

    @staticmethod
    def set_front_lifting_normal(is_touch):
        """ Set the state of the front lifting touch sensor for normal position """
        SensorData.is_front_lifting_normal = is_touch

    @staticmethod
    def get_front_stair_touch():
        """ Return the state of the front stair touch sensor """
        return SensorData.is_front_stair_touch

    @staticmethod
    def set_front_stair_touch(is_touch):
        """ Set the state of the front stair touch sensor """
        SensorData.is_front_stair_touch = is_touch
    
    @staticmethod
    def get_front_ground_touch():
        """ Return the state of the front ground touch sensor """
        return SensorData.is_front_ground_touch

    @staticmethod
    def set_front_ground_touch(is_touch):
        """ Set the state of the front ground touch sensor """
        SensorData.is_front_ground_touch = is_touch

    @staticmethod
    def get_back_lifting_extended_max():
        """ Return the state of the back lifting mechanism touch sensor for max extension """
        return SensorData.is_back_lifting_extended_max

    @staticmethod
    def set_back_lifting_extended_max(is_touch):
        """ Set the state of the back lifting mechanism touch sensor for max extension """
        SensorData.is_back_lifting_extended_max = is_touch

    @staticmethod
    def get_back_lifting_normal_touch():
        """ Return the state of the back lifting mechanism touch sensor for normal position """
        return SensorData.is_back_lifting_normal

    @staticmethod
    def set_back_lifting_normal_touch(is_touch):
        """ Set the state of the back lifting mechanism touch sensor for normal position"""
        SensorData.is_back_lifting_normal = is_touch
    
    @staticmethod
    def get_back_ground_touch():
        """ Return the state of the back ground touch sensor """
        return SensorData.is_back_ground_touch

    @staticmethod
    def set_back_ground_touch(is_touch):
        """ Set the state of the back ground touch sensor """
        SensorData.is_back_ground_touch = is_touch

    @staticmethod
    def get_front_dist():
        """ Return the distance of the front distance sensor """
        return SensorData.front_dist

    @staticmethod
    def set_front_dist(dist):
        """ Set the distance of the front distance sensor """
        SensorData.front_dist = dist

    @staticmethod
    def get_back_ground_dist():
        """ Return the distance of the back ground distance sensor """
        return SensorData.back_ground_dist

    @staticmethod
    def set_back_ground_dist(dist):
        """ Set the distance of the back ground distance sensor """
        SensorData.back_ground_dist = dist
