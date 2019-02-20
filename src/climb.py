"""The main control flow for climbing a stair"""

# pylint: disable=R0912

from data import SensorData
from control import stop

async def climb_upstairs(sensors: SensorData) -> None:
    """ Function to make Spencer start climbing up stairs"""
    # TODO(anyone): Stop all movement
    # TODO(anyone): SAFETY CHECKS STILL NEED TO BE DONE

    # TODO(anyone): Need to sense step
    # TODO(anyone): Use Jonathan's code to align

    # BE INFRONT OF THE STEP
    # Spencer is infront of a step, TODO(anyone): Check
    touching_step = False
    while not touching_step:
        if sensors.front_stair_touch.get():
            # We are touching the step we can continue
            touching_step = True
            stop()
        else:
            # TODO(anyone) Align step keep driving forward until we reach step
            pass


    # LIFT FRONT ABOVE STEP
    # TODO(anyone): Lift front until max or touch sensor is 0
    front_above_step = False
    while not front_above_step:
        if (not sensors.front_stair_touch.get() and not sensors.front_lifting_normal.get() and
                sensors.front_dist_0.get() >= 20 and sensors.front_dist_1.get() >= 20):
            # The front is above the step
            front_above_step = True
            stop()
        else:
            # The front is not above the step we need to continue
            # TODO(anyone): Lift the front more
            pass

    # PLACE FRONT ON STEP
    # TODO(anyone): Drive forward so middle is touching the step
    front_on_step = False
    while not front_on_step:
        if (sensors.front_ground_touch.get() and sensors.front_lifting_normal.get() and
                sensors.front_middle_stair_touch.get()):
            # Front is on the step we can continue
            front_on_step = True
        else:
            # Front is not on the step we need to drive forward or lower the front more
            if sensors.front_middle_stair_touch == 1:
                # Middle is touching the step
                # TODO(anyone): Lower the front until touching the step
                stop()
            else:
                # TODO(anyone): Drive forward until Middle is touching the step
                pass

    # TODO(anyone): Lower Both until front in normal or back is max
    max_movement = False
    while not max_movement:
        if sensors.front_lifting_normal == 1 and sensors.back_lifting_extended_max == 0:
            # The robot has moved the maximum it can for either lifting mechanism
            max_movement = True
            stop()
        else:
            #TODO(anyone): Continue to lift the robot up
            pass

    # TODO(anyone): Drive forward so middle is on the step

    # This bit can be quite tricky, if we still have the falling problem, we may
    # need to lift one of the lifting mechanisms. We will need to do this while
    # driving forward. Until we have met the conditions for being on the step
    on_step = False
    while not on_step:
        if sensors.front_ground_touch.get() and sensors.middle_ground_touch.get() and sensors.back_stair_touch.get():
            # The robot is on the step
            on_step = True
            stop()
        else:
            # The robot is not on the step
            # TODO(anyone): Drive forward and keep the lifting mechanisms at the limits of extension
            pass

    # TODO(anyone): Lift back until in normal position
    is_back_normal = False
    while not is_back_normal:
        if sensors.back_lifting_normal == 1:
            # Back is normal
            is_back_normal = True
            stop()
        else:
            # TODO(anyone): Continue lifting back until normal
            pass

    # TODO(anyone): Repeat above until at the top of the stairs

def on_stair():
    """ Function to check if the robot satisfies the condition to be on a step """

async def climb_downstairs():
    """ Function to make Spencer start climbing downstairs"""
    # TODO(anyone): Stop step climbing thread
    return

def climb_a_stair():
    """ Function to make Spencer climb a step """
    # TODO(anyone): Stop step climbing thread
    return
