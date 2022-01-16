# For the micro:bit RC car controller

RADIO_CHANNEL = 42  # radio channel: 0~255

from microbit import display, Image, accelerometer, sleep
from math import pi, atan2, sqrt
import radio

radio.config(group=RADIO_CHANNEL)
radio.on()

def rotationPitch():
    return atan2(
            accelerometer.get_y(), 
            sqrt(accelerometer.get_x() ** 2 + accelerometer.get_z() ** 2)
            ) * (180 / pi)

def rotationRoll():
    return atan2(
            accelerometer.get_x(), 
            sqrt(accelerometer.get_y() ** 2 + accelerometer.get_z() ** 2)
            ) * (180 / pi)

while True:
    pitch = rotationPitch()
    roll = rotationRoll()
    
    if pitch < -30:
        display.show(Image.ARROW_N)
        radio.send('forward')
    elif pitch > 30:
        display.show(Image.ARROW_S)
        radio.send('backward')
    elif roll > 30:
        display.show(Image.ARROW_E)
        radio.send('left')
    elif roll < -30:
        display.show(Image.ARROW_W)
        radio.send('right')
    else:
        display.show(Image.SQUARE)
        radio.send('stop')
        
    sleep(100)
