#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# Write your program here.
def main():
    ev3 = EV3Brick()
    my_motor = Motor(Port.A)
    motor_L = Motor(Port.B)
    motor_R = Motor(Port.C)
    engine = DriveBase(motor_L, motor_R, wheel_diameter = 40, axle_track=200)
    my_touch_sensor = TouchSensor(Port.S1)

    ev3.speaker.beep()

    engine.straight(1000)
    engine.turn(360)
    engine.stop()

    while True:
        if my_touch_sensor.pressed():
            my_motor.run_target(200, 90)
        if ev3.buttons.pressed():
            break


if __name__ == "__main__":
    main()