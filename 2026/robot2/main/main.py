#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pixycamev3.pixy2 import Pixy2
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'ev3dev'
client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)
# print('establishing connection...')
# client.connect(SERVER)
# print('connected!')
# # In this program, the client sends the first message and then waits for the
# # server to reply.
# mbox.send('hello!')
# mbox.wait()
# print(mbox.read())

# Defining constants
GAIN = 5    # Gain for motorspeed
basic_speed = 250

robot1 = EV3Brick()
LIFT_MOTOR = Motor(Port.A, positive_direction=Direction.CLOCKWISE)#run(speed), run_time(speed, time, then=Stop.HOLD, wait=True), run_angle(speed, rotation_angle, 
LEFT_MOTOR = Motor(Port.B, positive_direction=Direction.CLOCKWISE)#then=Stop.HOLD, wait=True), run_target(speed, target_angle, then=Stop.HOLD, wait=True), 
RIGHT_MOTOR = Motor(Port.C, positive_direction=Direction.CLOCKWISE)#run_until_stalled(speed, then=Stop.COAST, duty_limit=None), dc(duty), stop(), brake(), hold()
#MEDIUM_MOTOR = Motor(Port.D, positive_direction=Direction.CLOCKWISE)#speed(), angle(), reset_angle()
#pixy2 = Pixy2(port=1, i2c_address=0x54)

#touch = TouchSensor(Port.S2) # pressed()
colorA_sensor = ColorSensor(Port.S3) # color(), ambient(), reflection(), rgb()
#colorB_sensor = ColorSensor(Port.S2)
#sonic_sensor = UltrasonicSensor(Port.S4) # distance(), presence()

drive_base = DriveBase(left_motor=LEFT_MOTOR, right_motor=RIGHT_MOTOR, wheel_diameter=42, axle_track=143)
#straight(distance), turn(angle), settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration), drive(drive_speed, turn_rate), stop()
#distance(), angle(), state(), reset()
#drive_base.settings(straight_speed=700, straight_acceleration=400, turn_rate=70, turn_acceleration=400)
# normal drive_base settings = (97, 391, 78, 313), when changed to above returns (293, 500, 80, 300)

def move(speed_x):
    """Move robot when in _ACTIVE mode. DOES NOT WORK WITH DRIVEBASE ACTIVE"""
    speed_x *= GAIN
    LEFT_MOTOR.run(basic_speed - speed_x)
    RIGHT_MOTOR.run(basic_speed + speed_x)

def stop():
    """STOPS MOTORS WHEN INDIVIDUALLY USED, DOES NOT WORK WITH DRIVEBASE ACTIVE"""
    LEFT_MOTOR.stop()
    RIGHT_MOTOR.stop()
