#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,UltrasonicSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pixycamev3.pixy2 import Pixy2, MainFeatures, Pixy2Mode

#Intiialize bluetooth server
server = BluetoothMailboxServer()
mbox = TextMailbox('greeting', server)

# Defining constants
KP = 0.9      # Proportional constant PID-controller
KI = 0    # Integral constant PID-controller
KD = 1        # Derivative constant PID-controller
GAIN = 7    # Gain for motorspeed

robot1 = EV3Brick()
CLAW_MOTOR = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
LEFT_MOTOR = Motor(Port.B, positive_direction=Direction.CLOCKWISE) 
RIGHT_MOTOR = Motor(Port.C, positive_direction=Direction.CLOCKWISE)
MEDIUM_MOTOR = Motor(Port.D, positive_direction=Direction.CLOCKWISE)

colorA_sensor = ColorSensor(Port.S2) #Line follow sensor
colorB_sensor = ColorSensor(Port.S3) #Color detector
sonic_sensor = UltrasonicSensor(Port.S4) # distance(), presence()

drive_base = DriveBase(left_motor=LEFT_MOTOR, right_motor=RIGHT_MOTOR, wheel_diameter=60, axle_track=144)

def close_claw():
    CLAW_MOTOR.reset_angle(950)
    CLAW_MOTOR.run_target(500, 0)

def open_claw():
    CLAW_MOTOR.reset_angle(0)
    CLAW_MOTOR.run_target(500, 950)

def color_sense_follow():
    """General line follow and placing the first two pillars"""
    BLACK = 15
    WHITE = 100
    threshold = (BLACK + WHITE) / 2
    lastKD = 0
    integral = 0
    derivitive = 0

    # Set the drive speed at 100 millimeters per second.
    DRIVE_SPEED = 100

    while True:
        deviation =  (colorA_sensor.reflection() - threshold)*-1
        integral = integral + deviation
        derivitive = deviation - lastKD
        turn_rate = KP * deviation + KI * integral + KD * derivitive
        drive_base.drive(DRIVE_SPEED, turn_rate)
        lastKD = deviation
        
        if colorB_sensor.color() == Color.RED:
            drive_base.stop()
            break
        if colorB_sensor.color() == Color.BLACK:
            drive_base.stop()
            drive_base.turn(-80)

def color_sense_follow2():
    """Changed the color sense logic to assist placing the last two pillars"""
    BLACK = 15
    WHITE = 100
    threshold = (BLACK + WHITE) / 2
    lastKD = 0
    integral = 0
    derivitive = 0

    # Set the drive speed at 100 millimeters per second.
    DRIVE_SPEED = 100

    while True:
        deviation =  (colorA_sensor.reflection() - threshold)*-1
        integral = integral + deviation
        derivitive = deviation - lastKD
        turn_rate = KP * deviation + KI * integral + KD * derivitive
        drive_base.drive(DRIVE_SPEED, turn_rate)
        lastKD = deviation

        if colorB_sensor.color() == Color.BLACK:
            drive_base.stop()
            drive_base.turn(-80)
        if colorB_sensor.color() == Color.GREEN:
            drive_base.stop()
            break
        #print(colorA_sensor.reflection())
        
def mark_x():
    """Create a one inch X"""
    MEDIUM_MOTOR.reset_angle(0)
    RIGHT_MOTOR.reset_angle(0)
    MEDIUM_MOTOR.run_angle(150, 90)
    drive_base.straight(60)
    drive_base.stop()
    MEDIUM_MOTOR.run_angle(150, -90)
    RIGHT_MOTOR.reset_angle(0)
    RIGHT_MOTOR.run_target(200, 100)
    MEDIUM_MOTOR.run_angle(150, 90)
    drive_base.straight(-60)
    drive_base.stop
    MEDIUM_MOTOR.run_angle(150, -90)

def challenge_1():
    """Avoid 4 cones placed in a straight line while moving 
    from base camp to primary dig site"""
    color_sense_follow()

def challenge_2():
    """parthenon build"""
    #Pickup and place first pillar
    mbox.wait()
    message = mbox.read()
    if message == 'Continue':
        while sonic_sensor.distance() >= 85:
            drive_base.drive(150, 0)
        drive_base.stop()
        close_claw()
        drive_base.turn(-170)
        drive_base.straight(300)
        color_sense_follow()
        drive_base.straight(85)
        open_claw()
        drive_base.straight(-80)
        drive_base.turn(170)
        drive_base.straight(100)
        color_sense_follow()
        #Pickup and place second pillar
        while sonic_sensor.distance() >= 85:
            drive_base.drive(150, 0)
        drive_base.stop()
        close_claw()
        drive_base.turn(-170)
        color_sense_follow()
        drive_base.turn(80)
        drive_base.straight(50)
        color_sense_follow()
        open_claw()
        drive_base.straight(-80)
        drive_base.turn(125)
        drive_base.straight(150)
        color_sense_follow()
        #Pickup and place third pillar
        while sonic_sensor.distance() >= 85:
            drive_base.drive(150, 0)
        drive_base.stop()
        close_claw()
        drive_base.turn(-170)
        color_sense_follow2()
        drive_base.turn(80)
        drive_base.straight(120)
        open_claw()
        drive_base.straight(-130)
        drive_base.turn(80)
        color_sense_follow()
        #Pickup and place fourth pillar
        while sonic_sensor.distance() >= 85:
            drive_base.drive(150, 0)
        drive_base.stop()
        close_claw()
        drive_base.turn(-170)
        color_sense_follow2()
        drive_base.turn(-50)
        open_claw()
        drive_base.straight(-500)
        drive_base.turn(230)
    
def challenge_3():
    """Mark a 1" X at location of 3 buried artifacts in main dig site (must be 3" apart)"""
    mark_x()
    drive_base.straight(220)
    drive_base.stop()
    mark_x()
    drive_base.straight(220)
    drive_base.stop()
    mark_x()
    
def main():
    #The server must be started before the client!
    server.wait_for_connection()
    challenge_1()
    mbox.send("Go")
    challenge_2()
    mbox.send("Next")
    mbox.wait()
    message = mbox.read()
    if message == "Done":
        drive_base.turn()
        drive_base.straight(400)
        challenge_3()
    mbox.send('finished')
    mbox.wait()
    message2 = mbox.read()
    if message2 == "Play song":
        robot1.speaker.play_file('indiana_jones.wav')
       
if __name__ == '__main__':
    main()