import threading
import enum
import logging


SENSOR_DATA_LOG = logging.getLogger("SensorData")

class SensorData():
    """
    Contains the sensor data from the robot
    """

    # TODO(anyone) Comment beside the sensors the channel they are using

    # Distance sensors
    front_dist_0 = 0.0
    front_dist_1 = 0.0
    back_ground_dist = 0.0

    # Touch sensors
    is_back_ground_touch = 0
    is_back_lifting_normal = 0
    is_back_lifting_extended_max = 0

    is_front_ground_touch = 0
    is_front_stair_touch = 0
    is_front_lifting_normal = 0
    is_front_lifting_extended_max = 0 # Fully extended is true when touch sensor reads 0

    is_front_middle_stair_touch = 0

    # Distance sensors locks
    lock_front_dist_0 = threading.Lock()
    lock_front_dist_1 = threading.Lock()
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
    def get_front_dist_0():
        """ Return the distance of the front distance sensor """
        with SensorData.lock_front_dist_0:
            data = SensorData.front_dist_0
        return data

    @staticmethod
    def set_front_dist_0(dist):
        """ Set the distance of the front distance sensor """
        with SensorData.lock_front_dist_0:
            SensorData.front_dist_0 = dist

    @staticmethod
    def get_front_dist_1():
        """ Return the distance of the front distance sensor """
        with SensorData.lock_front_dist_1:
            data = SensorData.front_dist_1
        return data

    @staticmethod
    def set_front_dist_1(dist):
        """ Set the distance of the front distance sensor """
        with SensorData.lock_front_dist_1:
            SensorData.front_dist_1 = dist

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

    @staticmethod
    def add_to_sensor_data(name, value):
        """ Adds sensors data to the data structure """
        if name == Sensors.front_dist_0.name:
            SensorData.set_front_dist_0(value)

        elif name == Sensors.front_dist_1.name:
            SensorData.set_front_dist_1(value)

        elif name == Sensors.back_dist.name:
            SensorData.set_back_ground_dist(value)

        elif name == Sensors.back_ground_touch.name:
            SensorData.set_back_ground_touch(value)

        elif name == Sensors.back_lifting_normal_touch.name:
            SensorData.set_back_lifting_normal_touch(value)

        elif name == Sensors.back_lifting_extended_max_touch.name:
            SensorData.set_back_lifting_extended_max(value)

        elif name == Sensors.front_ground_touch.name:
            SensorData.set_front_ground_touch(value)

        elif name == Sensors.front_stair_touch.name:
            SensorData.set_front_stair_touch(value)

        elif name == Sensors.front_lifting_normal_touch.name:
            SensorData.set_front_lifting_normal(value)

        elif name == Sensors.front_lifting_extended_max_touch.name:
            SensorData.set_front_lifting_extended_max(value)

        elif name == Sensors.front_middle_stair_touch.name:
            SensorData.set_front_middle_stair_touch(value)

        else:
            #TODO(anyone): PANIC I don't know what to do here
            SENSOR_DATA_LOG.debug("Adding to data structure invalid name: %s", name)


class Sensors(enum.Enum):
    """ Enum for all the senors to make using them easier"""
    front_dist_0 = 0
    front_dist_1 = 1
    back_dist = 2
    back_ground_touch = 3
    back_lifting_normal_touch = 4
    back_lifting_extended_max_touch = 5
    front_ground_touch = 6
    front_stair_touch = 7
    front_lifting_normal_touch = 8
    front_lifting_extended_max_touch = 9
    front_middle_stair_touch = 10

