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
KP = 400     # Proportional constant PID-controller
KI = 1200   # Integral constant PID-controller
KD = 5   # Derivative constant PID-controller
GAIN = 5    # Gain for motorspeed
basic_speed = 250

robot1 = EV3Brick()
motor_a = Motor(Port.A, positive_direction=Direction.CLOCKWISE)#run(speed), run_time(speed, time, then=Stop.HOLD, wait=True), run_angle(speed, rotation_angle, 
motor_b = Motor(Port.B, positive_direction=Direction.CLOCKWISE)#then=Stop.HOLD, wait=True), run_target(speed, target_angle, then=Stop.HOLD, wait=True), 
motor_c = Motor(Port.C, positive_direction=Direction.CLOCKWISE)#run_until_stalled(speed, then=Stop.COAST, duty_limit=None), dc(duty), stop(), brake(), hold()
motor_d = Motor(Port.D, positive_direction=Direction.CLOCKWISE)#speed(), angle(), reset_angle()
pixy2 = Pixy2(port=1, i2c_address=0x54)

#touch = TouchSensor(Port.S2) # pressed()
colorA_sensor = ColorSensor(Port.S3) # color(), ambient(), reflection(), rgb()
colorB_sensor = ColorSensor(Port.S2)
sonic_sensor = UltrasonicSensor(Port.S4) # distance(), presence()

CLAW_MOTOR = motor_a
LEFT_MOTOR = motor_b
RIGHT_MOTOR = motor_c
MEDIUM_MOTOR = motor_d

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

def detect_colors(color_sig):
    try:
        nr_blocks, block = pixy2.get_blocks(color_sig, 255)
        return block[0] if block else None
    except AttributeError:
        return False                                                                                                     

def track_color(color_sig):
    X_REF = 158  # X-coordinate of referencepoint for color track screen size = (315, 207)
    Y_REF = 150  # Y-coordinate of referencepoint for color track screen size = (315, 207)
    
    #int8_t getBlocks(bool wait [optional], uint8_t sigmap [optional], uint8_t maxBlocks [optional])
    """getBlocks() gets all detected blocks in the most recent frame. The new data is then available in the blocks member variable. 
    The returned blocks are sorted by area, with the largest blocks appearing first in the blocks array. 
    It returns an error value (<0) if it fails and the number of detected blocks (>=0) if it succeeds."""
    # Request block
    nr_blocks, block = pixy2.get_blocks(color_sig, 255) # get_blocks(signature to look for, total blocks to look at)
    #nr_blocks = total number of blocks of allowed signatures, block = list of blocks received

    #If blocks are found 
    try:
        if nr_blocks > 0:
            # Find center of the block on (x, y)
            x = block[0].x_center # X-centrois of object
            y = block[0].y_center # Y-centroid of object
            #control for rotation (how far away is center of block from center of screen designated above as X_REF)
            dx = X_REF - x  # Error in reference to X_REF
            #control for forward/backward movement (how far away is center of block from center of screen designated above as Y_REF)
            dy = Y_REF - y  # Error in reference to Y_REF
            # Calculate motorspeed out of speed_x and speed_y
            # Use GAIN otherwise speed will be to slow, but limit in range [-1000,1000]
            rspeed = (dy - dx)
            lspeed = (dy + dx)
            RIGHT_MOTOR.run(speed = round(rspeed))
            LEFT_MOTOR.run(speed = round(lspeed))
        else:
            # SIG1 not detected, stop motors
            stop()
    except AttributeError:
        return

def avoid_to_left(color_sig):
    X_REF = 300 #(315, 207)
    nr_blocks, block = pixy2.get_blocks(color_sig, 255)
    try:
        if nr_blocks > 0:
            x = block[0].x_center
            dx = X_REF - x
            if x < X_REF:
                LEFT_MOTOR.run(speed = -dx)
                RIGHT_MOTOR.run(speed = dx)
        else:
            stop()
    except AttributeError:
        return

def avoid_to_right(color_sig):
    X_REF = 30 #(315, 207)
    nr_blocks, block = pixy2.get_blocks(color_sig, 255)
    try:
        if nr_blocks > 0:
            x = block[0].x_center
            dx = X_REF - x
            if x > X_REF:
                LEFT_MOTOR.run(speed = -dx)
                RIGHT_MOTOR.run(speed = dx)
        else:
            stop()    
    except AttributeError:
        return

def close_claw():
    CLAW_MOTOR.reset_angle(950)
    CLAW_MOTOR.run_target(500, 0)

def open_claw():
    CLAW_MOTOR.reset_angle(0)
    CLAW_MOTOR.run_target(500, 950)

def approach():
    X_REF = 39   # X-center coordinate of view for line follow  screen size = (78, 51)
    # Get linetracking data from pixy2
    data = pixy2.get_linetracking_data()
    # Process data
    if data.error:
        # Data error: unkown feature type, try reading again
        pass
    else:
        if data.number_of_barcodes > 0:
            for i in range(0, data.number_of_barcodes):
                if data.barcodes[i].y <= 39:
                    move(-2)
                if data.barcodes[i].y > 40:
                    move(2)
                
    
def line_follow():
    X_REF = 39   # X-center coordinate of view for line follow  screen size = (78, 51)
    # Get linetracking data from pixy2
    data = pixy2.get_linetracking_data()
    # Process data
    if data.error:
        # Data error: unkown feature type, try reading again
        pass
    else:
        if data.number_of_barcodes > 0:
            for i in range(0, data.number_of_barcodes):
                if data.barcodes[i].code == 0:
                    pass
                if data.barcodes[i].code == 1:
                    #Location of next challenge
                    return
                if data.barcodes[i].code == 2:
                    #Location of next challenge
                    pass
                if data.barcodes[i].code == 3:
                    #Location of next challenge
                    pass
                if data.barcodes[i].code == 4:
                    #Location of next challenge
                    pass
                if data.barcodes[i].code == 5:
                    pass
                if data.barcodes[i].code == 6:
                    pass
                if data.barcodes[i].code == 7:
                    pass
                if data.barcodes[i].code == 8:
                    pass
                if data.barcodes[i].code == 9:
                    pass
                if data.barcodes[i].code == 10:
                    pass
                if data.barcodes[i].code == 11:
                    pass
                if data.barcodes[i].code == 12:
                    pass
                if data.barcodes[i].code == 13:
                    pass
                if data.barcodes[i].code == 14:
                    pass
                if data.barcodes[i].code == 15:
                    pass
                    
    #Actual code to follow the line
    if data.number_of_vectors > 0:
        dx = X_REF - data.vectors[0].x1
        move(dx)
    else:
        # No vector data, stop robot
        stop()
    # Clear data for reading next loop
    data.clear()

def color_sense_follow():
    BLACK = 9
    WHITE = 85
    threshold = (BLACK + WHITE) / 2

    # Set the drive speed at 100 millimeters per second.
    DRIVE_SPEED = 100

    # Set the gain of the proportional line controller. This means that for every
    # percentage point of light deviating from the threshold, we set the turn
    # rate of the drivebase to 1.2 degrees per second.

    # For example, if the light value deviates from the threshold by 10, the robot
    # steers at 10*1.2 = 12 degrees per second.
    PROPORTIONAL_GAIN = 1.2

    while True:
        deviation = colorA_sensor.reflection() - threshold
        turn_rate = PROPORTIONAL_GAIN * deviation
        drive_base.drive(DRIVE_SPEED, turn_rate)

def mark_x():
    def color_check():
        while colorA_sensor.color() != Color.BROWN:
            if colorA_sensor.color() == Color.BLACK or colorA_sensor.color() == Color.BLUE:
                LEFT_MOTOR.run(20)
                RIGHT_MOTOR.run(17)
            else:
                LEFT_MOTOR.run(17)
                RIGHT_MOTOR.run(20)
    color_check()
    LEFT_MOTOR.run_angle(speed = 25, rotation_angle = 2)#Determine what 0.38 rotations is in degrees angle
    color_check()
    RIGHT_MOTOR.run_angle(speed = 25, rotation_angle = 12)#Determine what 1 rotation is in degrees angle
    color_check()
    LEFT_MOTOR.run_angle(speed = 25, rotation_angle = 4)#Determine what 0.38 rotations is in degrees angle
    color_check()
    LEFT_MOTOR.run_angle(speed = 25, rotation_angle = 5)#Determine what 0.38 rotations is in degrees angle
    color_check()
    RIGHT_MOTOR.run_angle(speed = 25, rotation_angle = 14)#Determine what 1 rotation is in degrees angle
    color_check()
    LEFT_MOTOR.run_angle(speed = 25, rotation_angle = 10)#Determine what 0.38 rotations is in degrees angle
    color_check()
    LEFT_MOTOR.run_angle(speed = 25, rotation_angle = 12)#Determine what 0.38 rotations is in degrees angle
    color_check()
    def unused_code():
        for i in range(3):
            MEDIUM_MOTOR.run_angle(speed = 25, rotation_angle = 87)
            LEFT_MOTOR.run_angle(speed = 25, rotation_angle = 2)#Determine what 0.3 rotations is in degrees angle
            RIGHT_MOTOR.run_angle(speed = 25, rotation_angle = 2)#Determine what 0.3 rotations is in degrees angle
            MEDIUM_MOTOR.run_angle(speed = 25, rotation_angle = -87)
            LEFT_MOTOR.run_angle(speed = 25, rotation_angle = 2)#Determine what 0.3 rotations is in degrees angle
            RIGHT_MOTOR.run_angle(speed = 25, rotation_angle = 2)#Determine what 0.3 rotations is in degrees angle
            LEFT_MOTOR.run_angle(speed = 1, rotation_angle = 12)#Determine what 1 rotations is in degrees angle
            RIGHT_MOTOR.run_angle(speed = 10, rotation_angle = 12)#Determine what 1 rotations is in degrees angle
            LEFT_MOTOR.run_angle(speed = -25, rotation_angle = 1)#Determine what 0.1 rotations is in degrees angle
            RIGHT_MOTOR.run_angle(speed = -25, rotation_angle = 1)#Determine what 0.1 rotations is in degrees angle
            MEDIUM_MOTOR.run_angle(speed = 25, rotation_angle = 87)
            LEFT_MOTOR.run_angle(speed = 25, rotation_angle = 2)#Determine what 0.3 rotations is in degrees angle
            RIGHT_MOTOR.run_angle(speed = 25, rotation_angle = 2)#Determine what 0.3 rotations is in degrees angle
            MEDIUM_MOTOR.run_angle(speed = 25, rotation_angle = -87)
            LEFT_MOTOR.run_angle(speed = 30, rotation_angle = 6)#Determine what 0.3 rotations is in degrees angle
            RIGHT_MOTOR.run_angle(speed = -30, rotation_angle = 6)#Determine what 0.3 rotations is in degrees angle

def pickup_number():
    pass

def estimate_distance():
    K = 1000  # from calibration
    data = pixy2.get_linetracking_data()
    # Process data
    if data.error:
        # Data error: unkown feature type, try reading again
        pass
    else:
        if data.number_of_barcodes > 0:
            for i in range(0, data.number_of_barcodes):
                if data.barcodes[i].code == 1:
                    print(data.barcodes[i].y)
    '''print("Distance:", distance, "cm")
    if width > 0:
        return K / width
    else:
        return None'''
    # after reading Pixy barcode block:

def site_map():
    color_line_follow(rotations=1.1)
    color_line_follow(direction='right', rotations=1)
    color_line_follow(rotations=1.15)
    color_line_follow(direction='right')
    color_line_follow()


def color_line_follow(l_speed = 150, r_speed = 150, direction='left', rotations=1):
    """Turn will be adjusted in code. Rotations multiplied by 360 degrees."""
    rotation = 360 * rotations
    for i in range(2):
        if colorA_sensor.color() == Color.BLUE and colorA_sensor.color() == Color.BLACK:
            while colorA_sensor.color() != Color.YELLOW or colorA_sensor.color() != Color.RED:
                LEFT_MOTOR.run(l_speed)
                RIGHT_MOTOR.run(r_speed + 5)
                print('color seen')
        else:
            while colorA_sensor.color() != Color.YELLOW or colorA_sensor.color() != Color.RED:
                LEFT_MOTOR.run(l_speed + 5)
                RIGHT_MOTOR.run(r_speed)
        if direction == 'left':
            LEFT_MOTOR.stop()
            RIGHT_MOTOR.reset_angle(0)
            RIGHT_MOTOR.run_target(r_speed, target_angle=rotation)
        if direction == 'right':
            RIGHT_MOTOR.stop()
            LEFT_MOTOR.reset_angle(0)
            LEFT_MOTOR.run_target(l_speed, target_angle=rotation)

def boulder_run(l_speed = 50, r_speed = 50, rotations=0.1):
    """Turn will be adjusted in code. Rotations multiplied by 360 degrees."""
    rotation = 360 * rotations
    for i in range(3):
        if colorA_sensor.color() == Color.BLUE or colorA_sensor.color() == Color.BLACK:
            while colorA_sensor.color() != Color.YELLOW:
                LEFT_MOTOR.run(l_speed)
                RIGHT_MOTOR.run(r_speed - 8)
        else:
            while colorA_sensor.color() != Color.YELLOW:
                LEFT_MOTOR.run(l_speed - 8)
                RIGHT_MOTOR.run(r_speed)
        LEFT_MOTOR.reset_angle(0)
        RIGHT_MOTOR.reset_angle(0)
        LEFT_MOTOR.run_target(l_speed, target_angle=rotation)
        RIGHT_MOTOR.run_target(r_speed, target_angle=rotation)

def challenge_1():
    """Avoid 4 cones placed in a straight line while moving 
    from base camp to primary dig site"""
    while True:
        line_follow()

    # if detect_colors(2):
    #     print("turning left")
    #     while detect_colors(2).x_center < 290:
    #         avoid_to_left(2)
    # drive_base.straight(160)
    # drive_base.turn(18)
    # drive_base.straight(220)
    # drive_base.turn(25)
    # drive_base.straight(110)
    # drive_base.stop()

    # if detect_colors(2):
    #     print("turning right")
    #     while detect_colors(2).x_center > 45:
    #         avoid_to_right(2)
    # drive_base.straight(100)
    # drive_base.turn(-18)
    # drive_base.straight(200)
    # drive_base.turn(-30)
    # drive_base.straight(110)
    # drive_base.stop()

    # if detect_colors(2):
    #     print("turning left")
    #     while detect_colors(2).x_center < 290:
    #         avoid_to_left(2)
    # drive_base.straight(160)
    # drive_base.turn(18)
    # drive_base.straight(220)
    # drive_base.turn(25)
    # drive_base.straight(110)
    # drive_base.stop()

    # if detect_colors(2):
    #     print("turning right")
    #     while detect_colors(2).x_center > 45:
    #         avoid_to_right(2)
    # drive_base.straight(100)
    # drive_base.turn(-18)
    # drive_base.straight(200)
    # drive_base.turn(-30)
    # drive_base.straight(110)
    # drive_base.stop()

def challenge_2():
    """Pickup and place 4 markers from equipment site 
    and place at the next 4 challenges to be completed in order"""
    line_follow()
    pickup_number()
    
def challenge_3():
    """Mark a 1" X at location of 3 buried artifacts in main dig site (must be 3" apart)"""
    line_follow()
    mark_x()

def challenge_4():
    """Navigate perimeter of main dig site and mark 4 corners
    bonus if 2nd bot circles main site twice and misses markers"""
    pass

def challenge_5():
    """Artifact Identifaction: Transport 2 tools, 2 art, and 2 fragments from artifact scatter area 
    to collections bins labeled Tools, Art, and Fragments
    Artifact Preservation: Place tops from equipment site on top of the 3 bins"""
    pass

def challenge_6():
    """Bot 1 brings artifacts with phrases: Ankh, Udja, Seneb, Em Hotep to bot 2.
    Bot 2 'scans' artifacts, spins in circle, and places artifacts in correct order"""
    pass

def challenge_7():
    """Place 2 ramps and a bridge that are 6" tall.  Climb the bridge and retrieve artifact.
    Carry artifact down to colection bin near platform"""
    pass

def challenge_8():
    """Retrieve parts from main dig site and take to reconstruction site. 
    Place four 8" pillars on a 12x12 base.  Place a 4" tall roof on the pillars."""
    i = 1
    while i <= 4:
        open_claw()
        while True:
            data = pixy2.get_linetracking_data()
            if data.number_of_vectors > 0:
                line_follow()
                data.clear()
            else: 
                break
        while sonic_sensor.distance() >= 85:
            drive_base.drive(50, 0)
        drive_base.stop()
        i += 1
        close_claw()

def challenge_9():
    """Retrieve an artifact that triggers a boulder run. Place artifact in bin without getting hit by boulder"""

def main():
    # The server must be started before the client!
    # print('waiting for connection...')
    # server.wait_for_connection()
    # print('connected!')
    # # In this program, the server waits for the client to send the first message
    # # and then sends a reply.
    # mbox.wait()
    # print(mbox.read())
    # mbox.send('hello to you!')

    #Code for challenges here
    site_map()

if __name__ == '__main__':
    main()