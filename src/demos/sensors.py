"""
A demo program which reads from an IR distance sensor
"""
import sys
import time
import traceback
from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput, VoltageRatioSensorType
from Phidget22.PhidgetException import ErrorCode, PhidgetException
from Phidget22.Phidget import ChannelClass, ChannelSubclass
# from Phidget22.Net import *

def print_open_error(e, ph):
    """Just prints some diagnostic information about opening a Phidget channel"""
    sys.stderr.write("Runtime Error -> Opening Phidget Channel: \n\t")
    display_error(e)
    if e.code == ErrorCode.EPHIDGET_TIMEOUT:
        sys.stderr.write("\nThis error commonly occurs if your device is not connected as specified, "
                         "or if another program is using the device, such as the Phidget Control Panel.\n")
        sys.stderr.write("\nIf your Phidget has a plug or terminal block for external power, ensure it is plugged in "
                         "and powered.\n")
        if (ph.getChannelClass() != ChannelClass.PHIDCHCLASS_VOLTAGEINPUT
                and ph.getChannelClass() != ChannelClass.PHIDCHCLASS_VOLTAGERATIOINPUT
                and ph.getChannelClass() != ChannelClass.PHIDCHCLASS_DIGITALINPUT
                and ph.getChannelClass() != ChannelClass.PHIDCHCLASS_DIGITALOUTPUT):
            sys.stderr.write("\nIf you are trying to connect to an analog sensor, you will need to use the "
                             "corresponding VoltageInput or VoltageRatioInput API with the appropriate SensorType.\n")

        if ph.getIsRemote():
            sys.stderr.write("\nEnsure the Phidget Network Server is enabled on the machine the Phidget is plugged "
                             "into.")

def display_error(e):
    """Prints out some additional information when you receive an error. Not
    actually important, just a useful aid.

    """
    sys.stderr.write("Desc: " + e.details + "\n")

    if e.code == ErrorCode.EPHIDGET_WRONGDEVICE:
        sys.stderr.write("\tThis error commonly occurs when the Phidget function you are calling does not match the "
                         "class of the channel that called it.\n"
                         "\tFor example, you would get this error if you called a PhidgetVoltageInput_* function with "
                         "a PhidgetDigitalOutput channel.")
    elif e.code == ErrorCode.EPHIDGET_NOTATTACHED:
        sys.stderr.write("\tThis error occurs when you call Phidget functions before a Phidget channel has been opened "
                         "and attached.\n"
                         "\tTo prevent this error, ensure you are calling the function after the Phidget has been "
                         "opened and the program has verified it is attached.")
    elif e.code == ErrorCode.EPHIDGET_NOTCONFIGURED:
        sys.stderr.write("\tThis error code commonly occurs when you call an Enable-type function before all Must-Set "
                         "Parameters have been set for the channel.\n"
                         "\tCheck the API page for your device to see which parameters are labled \"Must be Set\" on "
                         " the right-hand side of the list.")

def on_attach(ph):
    """When a sensor is attached, we configure it with various properties (interval between receiving inputs,
       minimum change required before we get an input, etc...)

    """
    ph.setDataInterval(1000)
    ph.setVoltageRatioChangeTrigger(0.0)
    if ph.getChannelSubclass() == ChannelSubclass.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT:
        print("\tSetting VoltageRatio SensorType")
        ph.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_VOLTAGERATIO)


def on_error(_ph, code, string):
    """We get error messages if the sensor receives values outside its operating parameters."""
    sys.stderr.write("[Phidget Error Event] -> " + string + " (" + str(code) + ")\n")

def on_voltage_change(_ph, voltage):
    """Here we handle the change event for the voltage"""
    print("[VoltageRatio Event] -> Voltage Ratio: " + str(voltage))

def on_sensor_change(_ph, value, unit):
    """The above event is processed by the Phidget API and converted into a distance."""
    print("[Sensor Event] -> Sensor Value: " + str(value) + unit.symbol)

def main():
    "The main function: loads an input and waits until terminated."
    try:
        try:
            channel = VoltageRatioInput()
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Creating VoltageRatioInput: \n\t")
            display_error(e)
            raise
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating VoltageRatioInput: \n\t" + e)
            raise

        channel.setChannel(0)
        channel.setOnAttachHandler(on_attach)
        channel.setOnErrorHandler(on_error)
        channel.setOnVoltageRatioChangeHandler(on_voltage_change)
        channel.setOnSensorChangeHandler(on_sensor_change)

        print("\nOpening and Waiting for Attachment...")

        try:
            channel.openWaitForAttachment(5000)
            # Set the sensor type to the 10-80cm distance one
            channel.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1101_SHARP_2Y0A21)
        except PhidgetException as e:
            print_open_error(e, channel)
            return

        print("Sampling data for 10 seconds.")

        while True:
            time.sleep(60)

        return
    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        display_error(e)
        traceback.print_exc()
        return
    finally:
        print("Cleaning up...")
        channel.setOnVoltageRatioChangeHandler(None)
        channel.setOnSensorChangeHandler(None)
        channel.close()


main()
