from gpiozero import LED
from time import sleep

green1 = LED(17)
yellow1 = LED(27)
red1 = LED(22)
green2 = LED(18)
yellow2 = LED(23)
red2 = LED(24)
green3 = LED(12)
yellow3 = LED(16)
red3 = LED(20)

def main():
    """Initialize all LEDs to be off"""
    green1.off()
    yellow1.off()
    red1.off()
    green2.off()
    yellow2.off()
    red2.off()
    green3.off()
    yellow3.off()
    red3.off()

    for i in range(10):
        cycle_light()

def cycle_light():
    """Alternate Green, Yellow, Red lights."""
    yellow2.off(), red3.on(), green1.on(), red1.off()
    sleep(3)
    green1.off(), yellow1.on()
    sleep(3)
    yellow1.off(), red1.on(), green2.on(), red2.off()
    sleep(3)
    green2.off(), yellow2.on()
    sleep(3)
    yellow2.off(), red2.on(), green3.on(), red3.off()
    sleep(3)
    green3.off(), yellow3.on()
    sleep(3)
    