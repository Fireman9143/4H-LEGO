#!/usr/bin/env pybricks-micropython
"""The first line looks like a comment.  It's called a shebang, and it tells the code interpreter what kind of program it's running"""

"""These imports are the suggested imports.  When you import the starter code from LEGO Mindstorms, these are the modules they recommend"""
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox, BluetoothMailboxClient


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
"""These are the variables that we create for our program.  Some of the pybricks modules need information given to them inside the parenthesisa"""
ev3 = EV3Brick()
left_motor=Motor(Port.B)  #Motor is a function inside the ev3devices module.  This function needs to know which port the motor is plugged into.  We hold that info in a variable to make it easy to use
right_motor=Motor(Port.C)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)  #DriveBase is a function inside the robotics module.  It needs data too.

ultra = UltrasonicSensor(Port.S4)
color = ColorSensor(Port.S3)
touch = TouchSensor(Port.S1)
gyro = GyroSensor(Port.S2)

# Write your program here.
ev3.speaker.beep()

# The following loop makes the robot drive forward until it detects an
# obstacle. Then it backs up and turns around. 
while True:
    robot.drive(200, 0)  # Begin driving forward at 200 millimeters per second.
    """Wait until an obstacle is detected. This is done by repeatedly
     doing nothing (waiting for 10 milliseconds) while the measured
     distance is still greater than 300 mm."""
    while ultra.distance() > 300:   #While the distance measured by the ultrasonic sensor is >300mm, execute the wait(10) code indented under the loop.  If <=300, exit the loop.
        wait(10)
    robot.straight(-300)  # Sending a new code to the robot DriveBase will stop the drive command and start this straight command.  Drive backward for 300 millimeters.
    robot.turn(120)   # Turn around by 120 degrees
    robot.stop()
    break  #ends the while True loop.  If you don't break out of the loop it will run forever!!


"""
#LINE FOLLOWER PROGRAM (remove the triple quotes at the start and end of the code)
BLACK = 9
WHITE = 85
threshold = (BLACK + WHITE) / 2    # Calculate the light threshold. Choose values based on your measurements.

DRIVE_SPEED = 100        # Set the drive speed at 100 millimeters per second.
PROPORTIONAL_GAIN = 1.2  # Set the gain of the proportional line controller. 
# This means that for every percentage point of light deviating from the threshold, we set the turn rate of the drivebase to 1.2 degrees per second.

# For example, if the light value deviates from the threshold by 10, the robot steers at 10*1.2 = 12 degrees per second.

while True:   #RUNS FOREVER!!!
    # Calculate the deviation from the threshold.
    deviation = line_sensor.reflection() - threshold

    # Calculate the turn rate.
    turn_rate = PROPORTIONAL_GAIN * deviation

    # Set the drive base speed and turn rate.
    robot.drive(DRIVE_SPEED, turn_rate)

    # You can wait for a short time or do other things in this loop.
    wait(10)
"""


#Bluetooth server example below
"""
# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

server = BluetoothMailboxServer()
mbox = TextMailbox('greeting', server)

# The server must be started before the client!
print('waiting for connection...')
server.wait_for_connection()
print('connected!')

# In this program, the server waits for the client to send the first message
# and then sends a reply.
mbox.wait()
print(mbox.read())
mbox.send('hello to you!')
"""

#Bluetooth client example below
"""
# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'ev3dev'

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)

print('establishing connection...')
client.connect(SERVER)
print('connected!')

# In this program, the client sends the first message and then waits for the
# server to reply.
mbox.send('hello!')
mbox.wait()
print(mbox.read())"""