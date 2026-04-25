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
SERVER = 'robot1'
client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)

# Defining constants
GAIN = 5    # Gain for motorspeed
basic_speed = 250

robot1 = EV3Brick()
LIFT_MOTOR = Motor(Port.D, positive_direction=Direction.CLOCKWISE)#run(speed), run_time(speed, time, then=Stop.HOLD, wait=True), run_angle(speed, rotation_angle, 
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

def color_sense_follow():
    BLACK = 7
    WHITE = 59
    threshold = (BLACK+WHITE/2)
    KP = 0.35
    KI = 0.0045
    KD = 4
    lastKD = 0
    integral = 0
    derivative = 0
    DRIVE_SPEED = 60

    while True:
        deviation = colorA_sensor.reflection() - threshold
        integral = integral + deviation
        derivative = deviation - lastKD
        turn_rate = KP * deviation + KI * integral + KD * derivative
        drive_base.drive(DRIVE_SPEED, turn_rate)
        lastKD = deviation
        if colorA_sensor.reflection() >=99:
            drive_base.stop()
            break

# def line_follow():
#     active = True
#     X_REF = 39   # X-center coordinate of view for line follow  screen size = (78, 51)
#     # Get linetracking data from pixy2
#     data = pixy2.get_linetracking_data()
#     # Process data
#     if data.error:
#         # Data error: unkown feature type, try reading again
#         pass
#     else:
#         if data.number_of_barcodes > 0:
#             for i in range(0, data.number_of_barcodes):
#                 if data.barcodes[i].code == 0:
#                     pass
#                 if data.barcodes[i].code == 1:
#                     #Pickup pillar 1
#                     active = False
#                     return active
#                 if data.barcodes[i].code == 2:
#                     #Pickup pillar 2
#                     active = False
#                     return active
#                 if data.barcodes[i].code == 3:
#                     #Pickup pillar 3
#                     active = False
#                     return active
#                 if data.barcodes[i].code == 4:
#                     #Pickup pillar 4
#                     active = False
#                     return active
#                 if data.barcodes[i].code == 5:
#                     #Turn left
#                     drive_base.turn(-90)
#                     drive_base.stop()
#                 if data.barcodes[i].code == 6:
#                     #Turn right
#                     drive_base.turn(90)
#                     drive_base.stop()
#                 if data.barcodes[i].code == 7:
#                     pass
#                 if data.barcodes[i].code == 8:
#                     pass
#                 if data.barcodes[i].code == 9:
#                     #Turn left
#                     drive_base.turn(-90)
#                     drive_base.stop()
#                 if data.barcodes[i].code == 10:
#                     pass
#                 if data.barcodes[i].code == 11:
#                     return False
#                 if data.barcodes[i].code == 12:
#                     pass
#                 if data.barcodes[i].code == 13:
#                     pass
#                 if data.barcodes[i].code == 14:
#                     pass
#                 if data.barcodes[i].code == 15:
#                     pass
                    
#     #Actual code to follow the line
#     if data.number_of_vectors > 0:
#         dx = X_REF - data.vectors[0].x1
#         move(dx)
#     else:
#         # No vector data, stop robot
#         stop()
#     # Clear data for reading next loop
#     data.clear()

def main():
    # print('establishing connection...')
    # client.connect(SERVER)
    # print('connected!')
    # # In this program, the client sends the first message and then waits for the
    # # server to reply.
    # mbox.send('hello!')
    # mbox.wait()
    # print(mbox.read())
    color_sense_follow()
    
if __name__ == '__main__':
    main()