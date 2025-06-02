#!/usr/bin/env pybricks-micropython

from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction
from pixycamev3.pixy2 import Pixy2, MainFeatures
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from time import sleep

def main():
    motor_a = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
    motor_d = Motor(Port.D, positive_direction=Direction.CLOCKWISE)
    drive = DriveBase(motor_a, motor_d, wheel_diameter=42, axle_track=143)
    cannon = Motor(Port.B, positive_direction=Direction.CLOCKWISE, gears=[12, 36])
    ev3 = EV3Brick()
    pixy2 = Pixy2(port=1, i2c_address=0x54)
    data=MainFeatures()
    basic_speed = 500
    GAIN = 10
    server = BluetoothMailboxServer()
    mbox = TextMailbox('greeting', server)
    next = True
    ev3.screen.print('waiting for connection...')
    server.wait_for_connection()
    ev3.screen.print('connected!')
    
    drive.straight(170)
    drive.turn(180)
    drive.stop()

    while True:
        response = coms(ev3, mbox)
        if response == 'start':
            next = True
            break
        else:
            sleep(1)

    while next:
        pixy2.set_lamp(1, 0)
        ev3.speaker.say("GO")
        ev3.screen.print("GOING")
        line_follow(brick=ev3, cam=pixy2, 
                    cannon=cannon,
                    data=data, 
                    motor_L=motor_a, 
                    motor_R=motor_d,
                    basic_speed=basic_speed,
                    GAIN=GAIN, 
                    wheel_base=drive)
        ev3.screen.print("Line follow finished")
        ev3.speaker.say("STOP")
        ev3.screen.print("Stopped")
        pixy2.set_lamp(0, 0)
        next = False

def shoot(brick, cannon):
    """Takes the cannon motor and rotates based on gearing for one revolution"""
    cannon.run_target(1000, 360, wait=True)
    cannon.reset_angle(0)

def line_follow(brick, cam, cannon, data, motor_L, motor_R, basic_speed, GAIN, wheel_base):
    """Takes all variables needed for Pixy Cam line follow.  Checks for barcodes for actions.
       wheel_base.turn activates the DriveBase module, which MUST be turned off by wheel_base.stop
       in order to go back to independant motor control for line follow."""
    X_REF=39 
    active = True
    good_count = 0
    bad_count = 0
    
    while active:
        if brick.buttons.pressed():
            cam.set_lamp(0, 0)
        if good_count + bad_count == 5:
            q_stop(motor_L, motor_R)
            active = False
        # Get linetracking data from pixy2
        data = cam.get_linetracking_data()
        # Process data
        if data.error:
            pass
        else:
            if data.number_of_barcodes > 0:
                # Barcode(s) found
                for i in range(0, data.number_of_barcodes):
                    if data.barcodes[i].code == 5:
                        q_stop(motor_L, motor_R)
                        brick.speaker.say('sector clear')
                        wheel_base.turn(180)
                        wheel_base.stop()
                    elif data.barcodes[i].code==13:
                        q_stop(motor_L, motor_R)
                        brick.speaker.say('enemy spotted')
                        shoot(brick, cannon)
                        brick.speaker.say('bogie down')
                        bad_count += 1
                        wheel_base.turn(180)
                        wheel_base.stop()
                    elif data.barcodes[i].code==14:
                        q_stop(motor_L, motor_R)
                        brick.speaker.say('friendly')
                        good_count += 1
                        wheel_base.turn(180)
                        wheel_base.stop()
        if data.number_of_vectors > 0:
            dx = X_REF - data.vectors[0].x1
            move(motor_L, motor_R, basic_speed, dx, GAIN)        
        else:
            # No vector data, stop robot
            q_stop(motor_L, motor_R)  
            #wheel_base.turn(10)
            #wheel_base.stop()
            #sleep(0.25)
        # Clear data for reading next loop
        data.clear()


def move(motor_L, motor_R, basic_speed, speed_x, GAIN):
    """Uses individual motors to correct for line follow based on Pixy Cam vector data"""
    speed_x *= GAIN
    speed_L = limit_speed(basic_speed - speed_x)
    speed_R = limit_speed(basic_speed + speed_x)
    motor_L.run(speed_L)
    motor_R.run(speed_R)


def limit_speed(speed):
  """Limit speed in range [-1000,1000]."""
  if speed > 1000:
    speed = 1000
  elif speed < -1000:
    speed = -1000
  return speed

def q_stop(motor_L, motor_R):
    """Stops each motor when driving with independant control for line follow"""
    motor_L.stop()
    motor_R.stop()

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!
def coms(brick, mbox):
    mbox.wait()
    return (mbox.read())
    

if __name__ == '__main__':
    main()