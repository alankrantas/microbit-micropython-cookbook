# micro:bit V2 MicroPython Cookbook (Updating)

![1](https://user-images.githubusercontent.com/44191076/79871966-c0ae8b00-8417-11ea-8255-cbc681d12b8d.jpg)

See also [BBC micro:bit MicroPython documentation](https://microbit-micropython.readthedocs.io/en/latest/index.html#)

This is the collection of my notes, tricks and experiments on BBC micro:bit and MicroPython. This guide has bee upgraded for micro:bit V2; most of them are compatible with V1 but there would be limitations.

## Something About micro:bit's MicroPython

micro:bit's MicroPython is developed by Damien George which is based on Python 3.4. So basically all built-in features in and before Python 3.4 can be used on micro:bit.

Since MicroPython is a dynamic language like Python, it requires more memory than other embedded langauges. But this is no longer an big issue for V2 which has 128k RAM instead of 16K on V1. It is also possible to run recursion algorithm without getting errors.

However, Bluetooth support are still unavailable in both version of firmwares.

## Ask Help From REPL

REPL (Read-Evaluate-Print-Loop) or "Serial" in the official editor is a very useful testing tool. You may need to press Ctrl + C to force the device to stop its current program and enter REPL mode.

List all modules:

```python
help('modules')
```

To see what's in a module or submodule/function/attribute:

```python
import microbit

help(microbit)  # display help content if there's any
help(microbit.pin0)
dir(microbit)  # list all members in this namespace
dir(microbit.pin0)
```

## Import * is a Bad Idea

in a lot of examples you may see

```python
from microbit import *
```

Import does not "read" a module or function into memory; what it really does is to add variables (name tags) pointing to all the stuff under module "microbit". So you can use these names directly without writing ```microbit.something```.

But using * to import everything is still a bad habit; in standard Python you might accidentally import something with same names and causing conflict. 

Instead, the better and clearer way is to write it like this:

```python
from microbit import pin0, display, sleep
```

## How Much Memory Left?

```python
from micropython import mem_info

print(mem_info(1))
```

You can also force micro:bit to free memory from time to time with garbage collection:

```python
import gc

gc.enable()  # enable automatic memory recycle
gc.collect()  # force memory recycle
```

## Classic Blinky

```python
from microbit import display, Image, sleep

while True:
    display.show(Image.HEART)
    sleep(1000)
    display.clear()
    sleep(1000)
```

## Roll a Dice

You might need to shake it harder to see changes. The gesture detection is not idel in micro:bit's MicroPython.

```python
from microbit import display, Image, accelerometer, sleep
from random import randint

dices = {  # dictionary of 5x5 dice images
    1: '00000:00000:00900:00000:00000',
    2: '00900:00000:00000:00000:00900',
    3: '90000:00000:00900:00000:00009',
    4: '90009:00000:00000:00000:90009',
    5: '90009:00000:00900:00000:90009',
    6: '90009:00000:90009:00000:90009',
}

while True:
    
    if accelerometer.is_gesture('shake'):
        display.show(Image(dices[randint(1, 6)]))
        sleep(500)
```

## Fill LED Display

Light up every LEDs in a specific brightness level (default max):

```python
from microbit import display, Image, sleep

def fillScreen(b=9):  # fill screen function, b = brightness (0-9)
    display.show(Image(':'.join([str(b) * 5] * 5)))


while True:
    # blink screen twice
    for _ in range(2):
        fillScreen()  # default = max brightness
        sleep(250)
        display.clear()
        sleep(250)
    
    sleep(500)
    
    # fade in
    for i in range(10):
        fillScreen(i)
        sleep(75)
    
    # fade out
    for i in reversed(range(10)):
        fillScreen(i)
        sleep(75)
        
    sleep(500)
```

## LED Bar Graph

A 25-level LED progress bar.

```python
from microbit import display, sleep

# bar graph function
def plotBarGraph(value, maxValue, b=9):
    bar = value / maxValue
    values = ((0.96, 0.88, 0.84, 0.92, 1.00), 
              (0.76, 0.68, 0.64, 0.72, 0.80),
              (0.56, 0.48, 0.44, 0.52, 0.60), 
              (0.36, 0.28, 0.24, 0.32, 0.40), 
              (0.16, 0.08, 0.04, 0.12, 0.20))
    for y in range(5):
        for x in range(5):
            display.set_pixel(x, y, b if bar >= values[y][x] else 0)


while True:
    lightLevel = display.read_light_level()
    plotBarGraph(lightLevel, 255)  # or plotBarGraph(lightLevel, 255, 9)
    sleep(50)
```

Since read_light_level() uses LEDs themselves as light sensors (see [this video](https://www.youtube.com/watch?v=TKhCr-dQMBY)), The LED screen would flicker a bit.

## Blinky LEDs Without Using Sleep

The two LEDs would blink at different intervals.

```python
from microbit import display
import utime

delay1, delay2 = 1000, 300
since1, since2 = utime.ticks_ms(), utime.ticks_ms()


while True:
    
    now = utime.ticks_ms()
    
    if utime.ticks_diff(now, since1) >= delay1:  # toogle LED (0, 0)
        display.set_pixel(0, 0, 9 if display.get_pixel(0, 0) == 0 else 0)
        since1 = utime.ticks_ms()
    
    if utime.ticks_diff(now, since2) >= delay2:  # toogle LED (4, 4)
        display.set_pixel(4, 4, 9 if display.get_pixel(4, 4) == 0 else 0)
        since2 = utime.ticks_ms()
```

## A More Convenient Pin Class?

Define a Pin class to repackage existing pin methods.

```python
from microbit import pin1, pin2, sleep

class Pin:
    
    __slots__ = ['pin']  # not to use dictionary to store attributes in order to save memory
    
    def __init__(self, pin):
        self.pin = pin
    
    def setPin(self, value):
        self.pin.write_digital(value)
    
    def setPWM(self, value):
        self.pin.write_analog(value)
    
    def getPin(self):
        self.pin.set_pull(self.pin.NO_PULL)
        return self.pin.read_digital()
        
    def getADC(self):
        try:
            return self.pin.read_analog()
        except:
            return 0
    
    def isPressed(self):
        self.pin.set_pull(self.pin.PULL_UP)
        return not self.pin.read_digital()
        
    def isTouched(self):
        try:
            self.pin.set_pull(self.pin.NO_PULL)
            return self.pin.is_touched()
        except:
            return False


led = Pin(pin1)  # external led at pin 1
button = Pin(pin2)  # external button at pin 2

while True:
    # light up LED when button is pressed
    led.setPin(button.isPressed())
    sleep(50)
```

Note: the external button needs to be "pulled up" with internal resistor so that micro:bit can read the input voltage change. Pin 5/11 (onboard button A/B) have their own internal pull-up resistors.

The external LED can be connected without a resistor, for the pin power output is 3.3V/6 mA only which is pretty harmless to any LEDs.

## Simpler Alternate Pin Class

Use **namedtuple** (a tuple that elements have attribute names) as a simple Pin class. We point the pin methods to these attributes.

```python
from microbit import pin1, pin2, sleep
from ucollections import namedtuple

Pin = namedtuple('Pin', ['setPin', 'setPWM', 'getPin', 'getADC', 'isTouched'])

def newPin(pin, pull_up=False):
    pin.set_pull(pin.PULL_UP if pull_up else pin.NO_PULL)
    return Pin(pin.write_digital, pin.write_analog, pin.read_digital, pin.read_analog, pin.is_touched)


led = newPin(pin1)
button = newPin(pin2, pull_up=True)

while True:
    led.setPin(not button.getPin())
    sleep(50)
```

## Value Mapping

Translate a value in a range to its corresponding value in anoher range, similar to **map()** in Arduino or micro:bit MakeCode. Borrowed from [here](https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another).

```python
from microbit import display, sleep

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)


while True:
    lightLevel = display.read_light_level()
    print(translate(lightLevel, 0, 255, 0, 1023))
    sleep(100)
```

## Servo Control

Note: currently (as for v2 beta) pin.set_analog_period throws ValueError and has been fixed in a future release.

```python
from microbit import pin0, sleep

def servoWrite(pin, degree):
    pin.set_analog_period(20)
    pin.write_analog(round((degree * 92 / 180 + 30), 0))


servoPin = pin0

while True:
    servoWrite(servoPin, 0)
    sleep(1000)
    servoWrite(servoPin, 180)
    sleep(1000)
```

Do not use servos and buzzers at the same time. They require different PWM frequencies and most microcontrollers can only use one frequency accross all pins at a time.

micro:bit V2 can output 190 mA from its 3V pin, which is enough for most hobby servos.


## Get Pitch and Roll Degrees

Similar to functions in micro:bit MakeCode. Be noted that these function cannot tell if the board is facing up or down. Probably need to use z axis readings for that.

Upload code and switch to REPL, you should see the output.

```python
from microbit import accelerometer, sleep
from math import pi, atan2, sqrt

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
    print('Pitch:', rotationPitch(), ' / roll:', rotationRoll())
    sleep(100)
```
## NeoPixel Rainbow/Rotation Effect

This code is based on Adafruit's example with adjustable brightness level.

```python
from microbit import pin0, sleep
from neopixel import NeoPixel
from micropython import const

led_num      = const(12)  # number of NeoPixels
led_maxlevel = const(128)  # light level (0-255)
led_delay    = const(0)  # NeoPixels cycle delay

np = NeoPixel(pin0, led_num)

def wheel(pos):
    r, g, b = 0, 0, 0
    if pos < 0 or pos > 255:
        r, g, b = 0, 0, 0
    elif pos < 85:
        r, g, b = 255 - pos * 3, pos * 3, 0
    elif pos < 170:
        pos -= 85
        r, g, b = 0, 255 - pos * 3, pos * 3
    else:
        pos -= 170
        r, g, b = pos * 3, 0, 255 - pos * 3
    r = round(r * led_maxlevel / 255)
    g = round(g * led_maxlevel / 255)
    b = round(b * led_maxlevel / 255)
    return (r, g, b)

def rainbow_cycle():
    global cycle
    for i in range(led_num):
        rc_index = (i * 256 // led_num) + cycle
        np[i] = wheel(rc_index & 255)
    np.show()
    sleep(led_delay)
    cycle = (cycle + 1) & 255


cycle = 0

while True:
    rainbow_cycle()
```

## Calcualte Fibonacci Sequence

[Fibonacci sequence](https://en.wikipedia.org/wiki/Fibonacci_number)

```python
from microbit import display

def Fibonacci(n):  # calculate nth number
    a = 0
    b = 1
    for i in range(n - 2):
        a, b = b, a + b
    return b

f = Fibonacci(42)
print(f)
display.scroll(f)
```

Why not a recursive version as well? Because the recursion depth is limited on micro:bits (V2 is a lot better than V1 but still quite limited) so it's not that ptractical to do so.

## Calcuate a List of Prime Numbers

Prime numbers (except 2, 3) are either 6n - 1 or 6n + 1. So we check if a number of 6n - 1/6n + 1 can be divided with any existing primes in the list. If not, it is a prime number and can be added to the list.

```python
from microbit import display

def find_primes(n):  # calculate primes up to n
    primes = [2, 3]
    for p in range(6, n + 1, 6):
        for p_test in range(p - 1, p + 2, 2):
            for prime in primes:
                if p_test % prime == 0:
                    break
            else:  # only execute when for is not exited by break
                primes.append(p_test)
    return primes


primes = find_primes(50)
print(primes)
for prime in primes:
    display.scroll(prime)
```

## Solving N-Queens Problems

[Eight queens puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle)

This one use recursion, and the recursion depth is not that big to be run on micro:bit V2. Of course, N > 10 will take like forever to calculate.

```python
import utime

maxQueens = 8  # N 
queens = [0] * maxQueens

def verifyPos(checkPos, newPos):
    for tmpPos in range(checkPos):
        if queens[tmpPos] == newPos or abs(tmpPos - checkPos) == abs(queens[tmpPos] - newPos):
            return False
    return True

def placeQueen(columnPos, maxNum):
    global counter, queens
    if columnPos == maxNum:
        counter += 1
        print(counter, queens)
    else:
        for newPos in range(1, maxNum + 1):
            if verifyPos(columnPos, newPos):
                queens[columnPos] = newPos
                placeQueen(columnPos + 1, maxNum)

counter = 0
startTime = utime.ticks_ms()
placeQueen(0, maxQueens)
timeDiff = utime.ticks_diff(utime.ticks_ms(), startTime) / 1000

print(counter, 'result(s) in', timeDiff, 'sec')
```

## Conway's Game of Life on 5x5 LED Display

[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

The program automatically reset the board when the number of cells dosen't change for a while.

```python
from microbit import display, sleep
from machine import reset
from random import randint

# Rule for B3/S23
# see https://www.conwaylife.com/wiki/List_of_Life-like_cellular_automata
Born    = '3'
Sustain = '23'

matrix = [bytearray((1 if randint(0, 2) == 0 else 0) 
            for _ in range(5)) for _ in range(5)]

def display_matrix():
    for i in range(5):
        for j in range(5):
            display.set_pixel(i, j, 9 if matrix[i][j] else 0)

def calculate_next_gen():
    global matrix
    matrix_buf = [bytearray(0 for _ in range(5)) for _ in range(5)]
    for i in range(5):
        for j in range(5):
            cell_num = 0
            for k in range(3):
                for l in range(3):
                    x = i + k - 1
                    y = j + l - 1
                    if x < 0:
                        x = 5 - 1
                    elif x >= 5:
                        x = 0 
                    if y < 0:
                        y = 5 - 1
                    elif y >= 5:
                        y = 0   
                    if matrix[x][y]:
                        cell_num += 1
            if not matrix[i][j]:
                matrix_buf[i][j] = 1 if str(cell_num) in Born else 0
            else:
                cell_num -= 1
                matrix_buf[i][j] = 1 if str(cell_num) in Sustain else 0
    matrix = matrix_buf

generation = 0
cell_count = 0
prev_cell_count = 0
cell_repeat = 0

while True:
    
    calculate_next_gen()
    cell_count = sum(map(sum, matrix))
    print(cell_count, 'cell(s)')
    display_matrix()
    
    if prev_cell_count == cell_count:
        cell_repeat += 1
    else:
        cell_repeat = 0
    prev_cell_count = cell_count
    
    if cell_count == 0 or cell_repeat >= 7:
        print('Resetting...')
        print('')
        sleep(500)
        reset()
        
    sleep(50)
```

The code would reset the micro:bit if there's no cell left or the cells are stable. Although sometimes it may be locked into a state with the same alternating cell numbers and need manual reset.

## Morse Code Machine

This allows you to enter your message into micro:bit and translate it to Morse code with the LED screen/buzzer. Go to the REPL mode and you'll see the promot.

```python
from microbit import display, Image, set_volume, sleep
from micropython import const
import music

set_volume(255)  # speaker volume (0-255)
morse_delay = const(75)  # morse code delay speed

# morse code table
morse_code = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
}
    
while True:
    
    print('Enter your message: (Press enter to exit)')
    msg_str = input('> ').upper()
    if not msg_str:
        break
    
    morse_str = ''.join([morse_code[s] for s in msg_str
                         if s in morse_code])
    print('Message converted:\n', morse_str)
    
    for code in morse_str:
        music.pitch(440)
        display.show(Image.TARGET)
        sleep(morse_delay * (3 if code == '-' else 1))
        music.stop()
        display.clear()
        sleep(morse_delay)
    
    print('')
```

## Radio Proximity Sensor

Load the code to two micro:bits. They will detect each other's radio signal strength and show it as LED bar graph. Can be used as an indoor treasure hunt game.

(This also works for micro:bit V1, however V1 is slower so there will be signal gap received by V2. So in order to mix V1 and V2, You'll have to either speed up V1 or slow down V2 loop delay.)

Due to some reason, the signal strength or RSSI changes very little regardless of transmite power. So I roughly remapped the value to 0-60 so that you can see the changes more clearly.

If there's no signal received the strength data would be set as zero.

```python
from microbit import display, sleep
import radio

def plotBarGraph(value, maxValue, b=9):
    bar = value / maxValue
    values = ((0.96, 0.88, 0.84, 0.92, 1.00), 
              (0.76, 0.68, 0.64, 0.72, 0.80),
              (0.56, 0.48, 0.44, 0.52, 0.60), 
              (0.36, 0.28, 0.24, 0.32, 0.40), 
              (0.16, 0.08, 0.04, 0.12, 0.20))
    for y in range(5):
        for x in range(5):
            display.set_pixel(x, y, b if bar >= values[y][x] else 0)


radio.config(group=42, power=7)
radio.on()

while True:
    
    radio.send('0')
    strength = 0.0
    data = radio.receive_full()
    
    if data:
        strength = data[1] + 255 - 155
    
    print('Signal strength:', strength)
    plotBarGraph(strength, 60)
    sleep(50)
```
