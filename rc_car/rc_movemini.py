# For Kitronik's Move:mini

RADIO_CHANNEL = 42  # radio channel: 0~255
LIGHT_LEVEL = 128

from microbit import display, Image, sleep, pin0, pin1, pin2
from neopixel import NeoPixel
import radio

radio.config(group=RADIO_CHANNEL)
radio.on()

class MoveMini:
    def __init__(self):
        self.np = NeoPixel(pin0, 5)
        self.pos = 0
        self.motor_right = pin1
        self.motor_left = pin2
        self.stop()
        
    def forward(self):
        display.show(Image.ARROW_N)
        self.np[1] = self.np[3] = (0, LIGHT_LEVEL, LIGHT_LEVEL)
        self.np[2] = (LIGHT_LEVEL, LIGHT_LEVEL, LIGHT_LEVEL)
        self.np[0] = self.np[4] = (0, 0, 0)
        self.np.show()
        self.motor_right.set_analog_period(20)
        self.motor_left.set_analog_period(20)
        self.motor_right.write_analog(50)
        self.motor_left.write_analog(100)
    
    def backward(self):
        display.show(Image.ARROW_S)
        self.np[1] = self.np[2] = self.np[3] = (LIGHT_LEVEL, 0, 0)
        self.np[0] = self.np[4] = (0, 0, 0)
        self.np.show()
        self.motor_right.set_analog_period(20)
        self.motor_left.set_analog_period(20)
        self.motor_right.write_analog(100)
        self.motor_left.write_analog(50)
    
    def left(self):
        display.show(Image.ARROW_W)
        self.np[1] = self.np[2] = (0, LIGHT_LEVEL, 0)
        self.np[0] = (LIGHT_LEVEL, LIGHT_LEVEL, 0)
        self.np[3] = self.np[4] = (0, 0, 0)
        self.np.show()
        self.motor_right.set_analog_period(20)
        self.motor_left.set_analog_period(20)
        self.motor_right.write_analog(100)
        self.motor_left.write_analog(100)
    
    def right(self):
        display.show(Image.ARROW_E)
        self.np[2] = self.np[3] = (0, LIGHT_LEVEL, 0)
        self.np[4] = (LIGHT_LEVEL, LIGHT_LEVEL, 0)
        self.np[0] = self.np[1] = (0, 0, 0)
        self.np.show()
        self.motor_right.set_analog_period(20)
        self.motor_left.set_analog_period(20)
        self.motor_right.write_analog(50)
        self.motor_left.write_analog(50)
    
    def stop(self):
        display.show(Image.HAPPY)
        for i in range(5):
            self.np[i] = (0, 0, 0)
        self.np.show()
        self.motor_right.read_digital()
        self.motor_left.read_digital()

car = MoveMini()

while True:
    sleep(25)
    
    direction = radio.receive()
    if direction == None:
        continue
    
    if direction == 'forward':
        car.forward()
    elif direction == 'backward':
        car.backward()
    elif direction == 'left':
        car.left()
    elif direction == 'right':
        car.right()
    else:
        car.stop()
    
