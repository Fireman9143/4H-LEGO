#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction
from pixycamev3.pixy2 import Pixy2, MainFeatures

def main():
    ev3 = EV3Brick()
    motor_a = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
    motor_d = Motor(Port.D, positive_direction=Direction.CLOCKWISE)
    
    pixy2 = Pixy2(port=1, i2c_address=0x54)
    data=MainFeatures()

    basic_speed = 500
    GAIN = 10
    X_REF=39 
    active = True
    
    while active:
        if ev3.buttons.pressed():
            pixy2.set_lamp(0, 0)

        # Get linetracking data from pixy2
        data = pixy2.get_linetracking_data()

        if data.number_of_vectors > 0:
            dx = X_REF - data.vectors[0].x1
            move(motor_a, motor_d, basic_speed, dx, GAIN)        
        else:
            # No vector data, stop robot
            q_stop(motor_a, motor_d)
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

if __name__ == '__main__':
    main()