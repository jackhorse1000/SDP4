import threading

class SensorData():
    """
    Contains the sensor data from the robot
    """

    # TODO(anyone) Comment beside the sensors the channel they are using

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

    # Distance sensors locks
    lock_front_dist = threading.Lock()
    lock_back_ground_dist = threading.Lock()

    # Locks for each touch sensor
    lock_back_ground_touch = threading.Lock()
    lock_back_lifting_normal = threading.Lock()
    lock_back_lifting_extended_max = threading.Lock()
    lock_front_ground_touch = threading.Lock()
    lock_front_stair_touch = threading.Lock()
    lock_front_lifting_normal = threading.Lock()
    lock_front_lifting_extended_max = threading.Lock()
    lock_front_middle_stair_touch = threading.Lock()

    @staticmethod
    def get_front_middle_stair_touch():
        """ Return the state of the front middle touch sensor for stair sensing """
        with SensorData.lock_front_middle_stair_touch:
            data = SensorData.is_front_middle_stair_touch
        return data

    @staticmethod
    def set_front_middle_stair_touch(is_touch):
        """ Set the state of the front middle touch sensor for stair sensing """
        with SensorData.lock_front_middle_stair_touch:
            SensorData.is_front_middle_stair_touch = is_touch

    @staticmethod
    def get_front_lifting_extended_max():
        """ Return the state of the front lifting touch sensor for max position """
        with SensorData.lock_front_lifting_extended_max:
            data = SensorData.is_front_lifting_extended_max
        return data

    @staticmethod
    def set_front_lifting_extended_max(is_touch):
        """ Set the state of the front lifting touch sensor for max position """
        with SensorData.lock_front_lifting_extended_max:
            SensorData.is_front_lifting_extended_max = is_touch

    @staticmethod
    def get_front_lifting_normal():
        """ Return the state of the front lifting touch sensor for normal position """
        with SensorData.lock_front_lifting_normal:
            data = SensorData.is_front_lifting_normal
        return data

    @staticmethod
    def set_front_lifting_normal(is_touch):
        """ Set the state of the front lifting touch sensor for normal position """
        with SensorData.lock_front_lifting_normal:
            SensorData.is_front_lifting_normal = is_touch

    @staticmethod
    def get_front_stair_touch():
        """ Return the state of the front stair touch sensor """
        with SensorData.lock_front_stair_touch:
            data = SensorData.is_front_stair_touch
        return data

    @staticmethod
    def set_front_stair_touch(is_touch):
        """ Set the state of the front stair touch sensor """
        with SensorData.lock_front_stair_touch:
            SensorData.is_front_stair_touch = is_touch
    
    @staticmethod
    def get_front_ground_touch():
        """ Return the state of the front ground touch sensor """
        with SensorData.lock_front_ground_touch:
            data = SensorData.is_front_ground_touch
        return data

    @staticmethod
    def set_front_ground_touch(is_touch):
        """ Set the state of the front ground touch sensor """
        with SensorData.lock_front_ground_touch:
            SensorData.is_front_ground_touch = is_touch

    @staticmethod
    def get_back_lifting_extended_max():
        """ Return the state of the back lifting mechanism touch sensor for max extension """
        with SensorData.lock_back_lifting_extended_max:
            data = SensorData.is_back_lifting_extended_max
        return data

    @staticmethod
    def set_back_lifting_extended_max(is_touch):
        """ Set the state of the back lifting mechanism touch sensor for max extension """
        with SensorData.lock_back_lifting_extended_max:
            SensorData.is_back_lifting_extended_max = is_touch

    @staticmethod
    def get_back_lifting_normal_touch():
        """ Return the state of the back lifting mechanism touch sensor for normal position """
        with SensorData.lock_back_lifting_normal:
            data = SensorData.is_back_lifting_normal
        return data

    @staticmethod
    def set_back_lifting_normal_touch(is_touch):
        """ Set the state of the back lifting mechanism touch sensor for normal position"""
        with SensorData.lock_back_lifting_normal:
            SensorData.is_back_lifting_normal = is_touch
    
    @staticmethod
    def get_back_ground_touch():
        """ Return the state of the back ground touch sensor """
        with SensorData.lock_back_ground_touch:
            data = SensorData.is_back_ground_touch
        return data

    @staticmethod
    def set_back_ground_touch(is_touch):
        """ Set the state of the back ground touch sensor """
        with SensorData.lock_back_ground_touch:
            SensorData.is_back_ground_touch = is_touch

    @staticmethod
    def get_front_dist():
        """ Return the distance of the front distance sensor """
        with SensorData.lock_front_dist:
            data = SensorData.front_dist
        return data

    @staticmethod
    def set_front_dist(dist):
        """ Set the distance of the front distance sensor """
        with SensorData.lock_front_dist:
            SensorData.front_dist = dist

    @staticmethod
    def get_back_ground_dist():
        """ Return the distance of the back ground distance sensor """
        with SensorData.lock_back_ground_dist:
            data = SensorData.back_ground_dist
        return data

    @staticmethod
    def set_back_ground_dist(dist):
        """ Set the distance of the back ground distance sensor """
        with SensorData.lock_back_ground_dist:
            SensorData.back_ground_dist = dist
