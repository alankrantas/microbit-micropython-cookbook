from microbit import display, Image, Sound, set_volume, accelerometer, sleep
from micropython import const
import audio, music, speech

max_score = const(5)  # number of games you have to pass (shake micro:bit to add on the level value)
add_level = const(10)  # max level can be added to the level value
drop_level = const(10)  # value that will auto subtracted from the level value
max_level = const(250)  # max level value to pass
volume = const(50)  # buzzer volume during gameplay (0~255)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def plotBarGraph(value, max_value, b=9):
    order = (23, 21, 20, 22, 24,
             18, 16, 15, 17, 19,
             13, 11, 10, 12, 14,
             8, 6, 5, 7, 9,
             3, 1, 0, 2, 4,)
    counter = 0
    display.clear()
    for y in range(5):
        for x in range(5):
            if value / max_value > order[counter] / 25:
                display.set_pixel(x, y, b)
            counter += 1

level = 0
score = 0
buzzer = True
set_volume(255)

display.clear()
audio.play(Sound.SPRING)
sleep(500)
numbers = ('One', 'Two', 'Three')
for i in range(3, 0, -1):
    display.show(i)
    speech.say(numbers[i-1], speed=500, pitch=50, throat=100, mouth=50)
    sleep(750)

set_volume(volume)

while score < max_score:
    shake = max(0, abs(accelerometer.get_x()) + abs(accelerometer.get_y()) + abs(accelerometer.get_z()) - 2048)
    level = min(max(0, level - drop_level + translate(shake, 0, 2048, 0, add_level)), max_level)
    pitch = round(translate(level, 0, max_level, 440, 880))
    plotBarGraph(level, max_level)
    if level == max_level:
        level = 0
        score += 1
        music.stop()
        sleep(50)
        display.show(Image.YES)
        music.play(music.BA_DING)
        sleep(450)
        continue
    if buzzer:
        music.pitch(pitch)
    else:
        music.stop()
    buzzer = not buzzer
    sleep(50)

set_volume(255)
sleep(500)
display.show(Image.HEART)
music.play(music.RINGTONE)
sleep(500)

while True:
    display.show(Image.HAPPY)
    sleep(500)
    display.clear()
    sleep(500)
