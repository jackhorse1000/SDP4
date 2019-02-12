import threading

class SensorData():
    """
    Contains the sensor data from the robot
    """

    # TODO(anyone) Comment beside the sensors below the channel they are using

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
        SensorData.lock_front_middle_stair_touch.acquire()
        try:
            data = SensorData.is_front_middle_stair_touch
        finally:
            SensorData.lock_front_middle_stair_touch.release()
        return data

    @staticmethod
    def set_front_middle_stair_touch(is_touch):
        """ Set the state of the front middle touch sensor for stair sensing """
        SensorData.lock_front_middle_stair_touch.acquire()
        try:
            SensorData.is_front_middle_stair_touch = is_touch
        finally:
            SensorData.lock_front_middle_stair_touch.release()

    @staticmethod
    def get_front_lifting_extended_max():
        """ Return the state of the front lifting touch sensor for max position """
        SensorData.lock_front_lifting_extended_max.acquire()
        try:
            data = SensorData.is_front_lifting_extended_max
        finally:
            SensorData.lock_front_lifting_extended_max.release()
        return data

    @staticmethod
    def set_front_lifting_extended_max(is_touch):
        """ Set the state of the front lifting touch sensor for max position """
        SensorData.lock_front_lifting_extended_max.acquire()
        try:
            SensorData.is_front_lifting_extended_max = is_touch
        finally:
            SensorData.lock_front_lifting_extended_max.release()

    @staticmethod
    def get_front_lifting_normal():
        """ Return the state of the front lifting touch sensor for normal position """
        SensorData.lock_front_lifting_normal.acquire()
        try:
            data = SensorData.is_front_lifting_normal
        finally:
            SensorData.lock_front_lifting_normal.release()
        return data

    @staticmethod
    def set_front_lifting_normal(is_touch):
        """ Set the state of the front lifting touch sensor for normal position """
        SensorData.lock_front_lifting_normal.acquire()
        try:
            SensorData.is_front_lifting_normal = is_touch
        finally:
            SensorData.lock_front_lifting_normal.release()

    @staticmethod
    def get_front_stair_touch():
        """ Return the state of the front stair touch sensor """
        SensorData.lock_front_stair_touch.acquire()
        try:
            data = SensorData.is_front_stair_touch
        finally:
            SensorData.lock_front_stair_touch.release()
        return data

    @staticmethod
    def set_front_stair_touch(is_touch):
        """ Set the state of the front stair touch sensor """
        SensorData.lock_front_stair_touch.acquire()
        try:
            SensorData.is_front_stair_touch = is_touch
        finally:
            SensorData.lock_front_stair_touch.release()
    
    @staticmethod
    def get_front_ground_touch():
        """ Return the state of the front ground touch sensor """
        SensorData.lock_front_ground_touch.acquire()
        try:
            data = SensorData.is_front_ground_touch
        finally:
            SensorData.lock_front_ground_touch.release()
        return data

    @staticmethod
    def set_front_ground_touch(is_touch):
        """ Set the state of the front ground touch sensor """
        SensorData.lock_front_ground_touch.acquire()
        try:
            SensorData.is_front_ground_touch = is_touch
        finally:
            SensorData.lock_front_ground_touch.release()

    @staticmethod
    def get_back_lifting_extended_max():
        """ Return the state of the back lifting mechanism touch sensor for max extension """
        SensorData.lock_back_lifting_extended_max.acquire()
        try:
            data = SensorData.is_back_lifting_extended_max
        finally:
            SensorData.lock_back_lifting_extended_max.release()
        return data

    @staticmethod
    def set_back_lifting_extended_max(is_touch):
        """ Set the state of the back lifting mechanism touch sensor for max extension """
        SensorData.lock_back_lifting_extended_max.acquire()
        try:
            SensorData.is_back_lifting_extended_max = is_touch
        finally:
            SensorData.lock_back_lifting_extended_max.release()

    @staticmethod
    def get_back_lifting_normal_touch():
        """ Return the state of the back lifting mechanism touch sensor for normal position """
        SensorData.lock_back_lifting_normal.acquire()
        try:
            data = SensorData.is_back_lifting_normal
        finally:
            SensorData.lock_back_lifting_normal.release()
        return data

    @staticmethod
    def set_back_lifting_normal_touch(is_touch):
        """ Set the state of the back lifting mechanism touch sensor for normal position"""
        SensorData.lock_back_lifting_normal.acquire()
        try:
            SensorData.is_back_lifting_normal = is_touch
        finally:
            SensorData.lock_back_lifting_normal.release()
    
    @staticmethod
    def get_back_ground_touch():
        """ Return the state of the back ground touch sensor """
        SensorData.lock_back_ground_touch.acquire()
        try:
            data = SensorData.is_back_ground_touch
        finally:
            SensorData.lock_back_ground_touch.release()
        return data

    @staticmethod
    def set_back_ground_touch(is_touch):
        """ Set the state of the back ground touch sensor """
        SensorData.lock_back_ground_touch.acquire()
        try:
            SensorData.is_back_ground_touch = is_touch
        finally:
            SensorData.lock_back_ground_touch.release()

    @staticmethod
    def get_front_dist():
        """ Return the distance of the front distance sensor """
        SensorData.lock_front_dist.acquire()
        try:
            data = SensorData.front_dist
        finally:
            SensorData.lock_front_dist.release()
        return data

    @staticmethod
    def set_front_dist(dist):
        """ Set the distance of the front distance sensor """
        SensorData.lock_front_dist.acquire()
        try:
            SensorData.front_dist = dist
        finally:
            SensorData.lock_front_dist.release()

    @staticmethod
    def get_back_ground_dist():
        """ Return the distance of the back ground distance sensor """
        SensorData.lock_back_ground_dist.acquire()
        try:
            data = SensorData.back_ground_dist
        finally:
            SensorData.lock_back_ground_dist.release()
        return data

    @staticmethod
    def set_back_ground_dist(dist):
        """ Set the distance of the back ground distance sensor """
        SensorData.lock_back_ground_dist.acquire()
        try:
            SensorData.back_ground_dist = dist
        finally:
            SensorData.lock_back_ground_dist.release()
