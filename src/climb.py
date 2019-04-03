"""The main control flow for climbing a stair"""

# pylint: disable=R0912

import asyncio
import logging

from data import SensorData
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
        left, right = self.sensors.front_dist_1, self.sensors.front_dist_0
        failure = 0
        LOG.info("Attempting to align against a wall. This is gonna go badly.")
        while self.sensors.get_moving():
            if failure > 10:
                LOG.error("front_up aborting due to too many failed reads")
                return False

            # If only one is valid, rotate towards the valid sensor
            if left.valid and left.value >= 10 and not right.valid:
                control.turn_left()
            elif right.valid and right.value >= 10 and not left.valid:
                control.turn_right()

            # If neither are valid, then drive forward.
            elif not left.valid or not right.valid:
                control.forward()
            else:
                failure = 0
                distance = min(left.value, right.value)
                delta = left.value - right.value
                LOG.debug("Distance=%f, delta=%f", distance, delta)

                # If we're a long way away, continue to move forward
                if distance >= 25:
                    control.forward()

                # Attempt to align against the wall
                elif delta > 0.75:
                    control.turn_right(0.4 if not (delta > 5) else 1)
                elif delta < -0.75:
                    control.turn_left(0.4 if not (delta < -5) else 1)
                elif distance <= 6:
                    control.stop()
                    return True

                # We're now aligned, but still a way away - move closer!
                else:
                    control.forward()

            await asyncio.sleep(SLEEP)

        LOG.error("Stopping due to no longer moving.")
        return False

    async def downstairs_find_wall(self) -> bool:
        """Attempt to find a wall and align itself against it.
          Returns when we are reasonable aligned to the step in front."""
        left, right = self.sensors.front_dist_1, self.sensors.front_dist_0
        failure = 0
        LOG.info("Attempting to align against a wall. This is gonna go badly.")
        while self.sensors.get_moving():
            if failure > 3:
                LOG.error("aborting align wall due to too many failed reads")
                return True

            # If only one is valid, rotate towards the valid sensor
            if left.valid and left.value >= 10 and not right.valid:
                control.turn_left()
            elif right.valid and right.value >= 10 and not left.valid:
                control.turn_right()

            # If neither are valid, then we must be too far or too close.
            elif not left.valid or not right.valid:
                failure += 1
            else:
                failure = 0
                distance = min(left.value, right.value)
                delta = left.value - right.value
                LOG.debug("Distance=%f, delta=%f", distance, delta)

                # If we're a long way away, no point aligning
                if distance >= 25:
                    # return True too far away to align
                    return True

                # Attempt to align against the wall
                if delta > 0.75:
                    control.turn_right(0.6 if not (delta > 5) else 1)
                elif delta < -0.75:
                    control.turn_left(0.6 if not (delta < -5) else 1)
                else:
                    control.stop()
                    return True
            await asyncio.sleep(SLEEP)
        LOG.error("Stopping due to no longer moving.")
        return False
