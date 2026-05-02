#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor)
from pybricks.parameters import Port, Direction, Color
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# This is the name of the remote EV3 we are connecting to.
SERVER = 'robot2'

client = BluetoothMailboxClient()
mbox = TextMailbox(name='greeting', connection=client)

# Defining constants
KP = 1.5
KI = 0
KD = 2
GAIN = 7    # Gain for motorspeed in the move function
basic_speed = 300

robot1 = EV3Brick()
LIFT_MOTOR = Motor(Port.D, positive_direction=Direction.CLOCKWISE)
LEFT_MOTOR = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
RIGHT_MOTOR = Motor(Port.C, positive_direction=Direction.CLOCKWISE)

colorA_sensor = ColorSensor(Port.S3) #Line follow sensor
colorB_sensor = ColorSensor(Port.S1) #Color detect sensor

drive_base = DriveBase(left_motor=LEFT_MOTOR, right_motor=RIGHT_MOTOR, wheel_diameter=60, axle_track=200)
last_height=0

def raise_forks(height=3800):
    global last_height
    LIFT_MOTOR.reset_angle(0)
    LIFT_MOTOR.run_target(speed=1000, target_angle=height)
    last_height = height

def lower_forks(this_height=0):
    LIFT_MOTOR.reset_angle(this_height)
    LIFT_MOTOR.run_target(speed=-1000, target_angle=0)

def color_sense_follow():
    """Use the color sensor to line follow."""
    BLACK = 9
    WHITE = 63
    threshold = (BLACK+WHITE/2)
    lastKD = 0
    integral = 0
    derivative = 0
    DRIVE_SPEED = 100

    while True:
        deviation = colorA_sensor.reflection() - threshold
        integral = integral + deviation
        derivative = deviation - lastKD
        turn_rate = KP * deviation + KI * integral + KD * derivative
        drive_base.drive(speed=DRIVE_SPEED, turn_rate=turn_rate)
        lastKD = deviation
        if colorB_sensor.color() == Color.GREEN:
            drive_base.stop()
            break

def challenge_1():
    """Line follow around the cones"""
    raise_forks(height=2200)
    color_sense_follow()

def challenge_2():
    """Parthenon build.  Pickup and place roof"""
    drive_base.settings(straight_speed=200, straight_acceleration=400, turn_rate=30, turn_acceleration=400)
    drive_base.straight(distance=100)
    color_sense_follow()
    lower_forks(last_height)
    drive_base.straight(distance=400)
    raise_forks()
    drive_base.turn(angle=118)
    drive_base.straight(distance=125)
    color_sense_follow()
    drive_base.turn(angle=-10)
    drive_base.straight(distance=300)
    color_sense_follow()
    drive_base.straight(distance=20)
    raise_forks(height=-1200)
    drive_base.straight(distance=-250)
    raise_forks(height=-2600)

def challenge_3():
    """After placing the roof, this will turn and travel to the idol for the temple run."""
    drive_base.turn(angle=-110)
    while True:
        drive_base.drive(speed=200, turn_rate=0)
        if colorB_sensor.color() == Color.BLUE:
            drive_base.stop()
            break
    drive_base.turn(angle=45)
    color_sense_follow()
    drive_base.turn(angle=45)
    drive_base.straight(distance=150)
    color_sense_follow()
    raise_forks()
    mbox.send("Play song")
    drive_base.straight(distance=500)
    lower_forks(last_height)
    drive_base.straight(distance=-500)

def main():
    """The main funciton brings all the code together as a master function."""
    client.connect(brick=SERVER)
    mbox.wait()
    message = mbox.read()
    if message == "Go": #When the first robot is clear, tell this robot to start cones
        challenge_1()
    mbox.wait() #Once the cone line follow is done, wait for this robot's turn to get roof
    message2 = mbox.read()
    if message2 == "Next": #When the pillars are in place, pickup the roof
        challenge_2()
        mbox.send("Done")
    mbox.wait()
    message3=mbox.read()
    if message3 == "finished":
        challenge_3()

if __name__ == '__main__':
    main()