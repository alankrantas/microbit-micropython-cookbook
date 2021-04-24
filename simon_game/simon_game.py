# Simon Game on BBC micro:bit V2
# by Alan Wang

"""
How to play:

1) Upload the script as main.py or in the form of .hex file.
2) After the welcome effects, press A + B to start.
3) Memorize the Simon sequence in each turn.
4) Tilt the board toward indicated directions to match the sequence.
5) After each tilting gesture, you have to return it to horizontal position.
6) Game will end when you failed.
7) There is no limit how long the Simon sequence can go.
"""

# import modules

from microbit import display, Image, Sound, sleep
from microbit import button_a, button_b, accelerometer
import random, music, audio, speech


# prepare data

"""
Note: the indexes of the following tuple represent
0 = toward up/north
1 = toward left/west
2 = toward right/east
3 = toward down/south

Since gesture "up" in micro:bit means "north side up",
I inverted the direction here.
But you can change the items of gestures, images and notes
to customize what would be shown and play on micro:bit.
"""

gestures = ('down', 'left', 'right', 'up')
images = (Image('69996:06960:00600:00000:00000:'),
          Image('60000:96000:99600:96000:60000:'),
          Image('00006:00069:00699:00069:00006:'),
          Image('00000:00000:00600:06960:69996:'),
          Image('30003:60006:90009:60006:30003:'))
notes = (262, 330, 392, 523)
simon = []
guess = []


# start up effects

display.clear()
audio.play(Sound.GIGGLE)
sleep(1000)
display.show(Image.FABULOUS)
speech.say('Simon says', speed=150, pitch=50, throat=100, mouth=50)
sleep(500)


# wait for the user to press A + B

display_flag = True
while not (button_a.is_pressed() and button_b.is_pressed()):
    if display_flag:
        display.show(images[4])
    else:
        display.clear()
    sleep(200)
    display_flag = not display_flag

for i in range(4):
    music.pitch(notes[i])
    display.show(images[i])
    sleep(100)

display.clear()
sleep(400)
music.stop()
sleep(1000)


# start game

while True:
    guess.clear()
    simon.append(random.randrange(4))  # add a random number to sequence
    
    for n in simon:
        music.pitch(notes[n])
        display.show(images[n])
        sleep(500)
        music.stop()
        display.clear()
        sleep(250)
        
    sleep(500)
    
    # game loop
    # the loop will end when user matched the whole sequence
    while len(guess) < len(simon):
        gesture = None
        display.show('?')
        
        # record user's tilting gestures
        for i in range(4):
            if accelerometer.was_gesture(gestures[i]):
                gesture = i
                break
        if gesture == None:
            continue
        guess.append(gesture)
        display.show(images[gesture])
        music.pitch(notes[gesture])
        sleep(250)
        music.stop()
        display.clear()
        sleep(100)
        
        # if the gesture don't match, exit the game loop
        if guess != simon[:len(guess)]:
            break
    
    else:
        # sequence successfully matched, go to next round
        display.show(Image.YES)
        music.play(music.POWER_UP)
        sleep(500)
        display.clear()
        sleep(500)
        continue
    
    # failed to match sequence
    sleep(100)
    display.show(Image.NO)
    music.play(music.WAWAWAWAA)
    break


# display final score

sleep(1000)
audio.play(Sound.HAPPY)

while True:
    display.scroll('SCORE: {}'.format(len(simon) - 1))
    sleep(1000)
