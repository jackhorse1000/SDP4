"""The main control flow for climbing a stair"""

# pylint: disable=R0912

import asyncio
import logging

from data import SensorData
# from autonomous_control import stop, forward
import autonomous_control as control

LOG = logging.getLogger("climb")

# The time to sleep between each computation step
SLEEP = 0.05

class ClimbController:
    """The main controller for Spencer, reading from sensor input and
       executing work on the motors."""

    sensors = None # type: SensorData

    def __init__(self, sensors: SensorData) -> None:
        self.sensors = sensors

    async def find_wall(self) -> bool:
        """Attempt to find a wall and align itself against it. Returns True if
           we're within 5 blocks of a wall, or False otherwise."""
        left, right = self.sensors.front_dist_0, self.sensors.front_dist_1
        failure = 0
        while True:
            if failure > 10:
                LOG.error("front_up aborting due to too many failed reads")
                return False

            if not left.valid or not right.valid:
                failure = failure + 1
            else:
                failure = 0
                distance = min(left.value, right.value)
                delta = left.value - right.value
                LOG.debug("Distance=%f, delta=%f", distance, delta)

                # If we're a long way away, continue to move forward
                if distance >= 10:
                    control.forward()

                # Attempt to align against the wall
                elif delta > 0.5:
                    control.turn_right()
                elif delta < -0.5:
                    control.turn_left()
                elif distance <= 7:
                    control.stop()
                    return True

                # We're now aligned, but still a way away - move closer!
                else:
                    control.forward()

            await asyncio.sleep(SLEEP)

    async def front_up(self) -> bool:
        """Move the front lifting segment up until we no longer have a wall in
           front of us.

        """

        left, right = self.sensors.front_dist_0, self.sensors.front_dist_1

        control.lift_front()
        failure = 0
        while True:
            if failure > 1 / SLEEP:
                LOG.error("front_up aborting due to too many failed reads")
                return False

            if not left.valid and not right.valid:
                failure = failure + 1
            else:
                distance = max(left.value if left.valid else 0, right.value if right.valid else 0)
                LOG.debug("Distance=%f", distance)

                if distance > 12:
                    # We've reached the top, coast a little bit more and stop.

                    # FIXME: Oh goodness, this is such a horrible hack. We're missing any sensors
                    # right now to determine if we're at the top though.
                    LOG.info("Reached the distance")
                    await asyncio.sleep(1.2)
                    LOG.info("Stopping")
                    control.stop()
                    await asyncio.sleep(1)
                    LOG.info("Finished waiting")
                    return True

            await asyncio.sleep(SLEEP)

    async def front_forward(self) -> None:
        """When we're approaching a wall, move forward until we're hard up
           against it.

        """
        control.forward()
        # TODO: Please release me from this mortal coil.
        await asyncio.sleep(1)
        control.stop()

    async def front_brace(self) -> bool:
        """Lower the front mechanism down until it's hard up against the
           floor.

        """
        touch = self.sensors.front_ground_touch
        failure = 0
        while True:
            if failure > 1 / SLEEP:
                LOG.error("front_approach_down aborting due to too many failed reads")
                return False

            if not touch.valid:
                failure = failure + 1
            elif touch.get():
                control.stop()
                return True
            else:
                control.lower_front()
            await asyncio.sleep(SLEEP)

    async def lift(self) -> None:
        """Lift both mechanisms until we're at the top."""
        control.lower_both()
        await asyncio.sleep(5)
        control.stop()

    async def work(self):
        """The main "worker" method for lifting up a stair. We'll probably make
           this more sane in the future.

        """
        try:
            # if not await self.find_wall():
            #     return False

            # await asyncio.sleep(0.1)

            # if not await asyncio.wait_for(self.front_up(), timeout=5):
            #     return False

            # await asyncio.wait_for(self.front_forward(), timeout=3)
            if not await asyncio.wait_for(self.front_brace(), timeout=1.2):
                return False

            await self.lift()
        finally:
            control.stop()

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
            control.stop()
        else:
            # TODO(anyone) Align step
            control.forward()


    # LIFT FRONT ABOVE STEP
    # TODO(anyone): Lift front until max or touch sensor is 0
    front_above_step = False
    while not front_above_step:
        if (not sensors.front_stair_touch.get() and not sensors.front_lifting_normal.get() and
                sensors.front_dist_0.get() >= 20 and sensors.front_dist_1.get() >= 20):
            # The front is above the step
            front_above_step = True
            control.stop()
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
                control.stop()
            else:
                # TODO(anyone): Drive forward until Middle is touching the step
                pass

    # TODO(anyone): Lower Both until front in normal or back is max
    max_movement = False
    while not max_movement:
        if sensors.front_lifting_normal == 1 and sensors.back_lifting_extended_max == 0:
            # The robot has moved the maximum it can for either lifting mechanism
            max_movement = True
            control.stop()
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
            control.stop()
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
            control.stop()
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


if __name__ == "__main__":
    def _main():
        import log
        log.configure()

        loop = asyncio.get_event_loop()
        loop.set_exception_handler(log.loop_exception_handler)

        data = SensorData()

        try:
            with data.front_dist_0, data.front_dist_1, data.front_ground_touch:
                controller = ClimbController(data)
                loop.create_task(controller.work())
                loop.run_forever()
        finally:
            loop.close()
            control.stop()
    _main()
