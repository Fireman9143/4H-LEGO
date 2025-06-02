#!/usr/bin/env pybricks-micropython

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!

from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.hubs import EV3Brick
from time import sleep
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port, Direction


def main():
    SERVER = 'ev3dev' # This is the name of the remote EV3 or PC we are connecting to.
    scorebot = EV3Brick()
    med_motor = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
    button = TouchSensor(Port.S1)

    client = BluetoothMailboxClient()
    mbox = TextMailbox('greeting', client)

    scorebot.screen.print('establishing connection...')
    client.connect(SERVER)
    scorebot.screen.print('connected!')

    active = True
    while active:
        if button.pressed():
            scorebot.speaker.say('scanning')
            med_motor.run(200)
            scorebot.speaker.play_file('684783__muray__sonar_830hz_synthesized.wav')
            med_motor.stop()
            scorebot.speaker.say('scan complete')
            active = False

    # In this program, the client sends the first message and then waits for the
    # server to reply.
    mbox.send('start')

if __name__ == '__main__':
    main()