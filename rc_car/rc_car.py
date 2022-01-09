# For the micro:bit RC car

RADIO_CHANNEL = 42  # radio channel: 0~255

from microbit import display, Image, sleep, pin1, pin2, pin8, pin12
import radio

radio.config(group=RADIO_CHANNEL)
radio.on()

motor_right_A = pin1
motor_right_B = pin2
motor_left_A = pin8
motor_left_B = pin12

motor_right_A.write_digital(0)
motor_right_B.write_digital(0)
motor_left_A.write_digital(0)
motor_left_B.write_digital(0)

while True:
    direction = radio.receive()
    if direction == None:
        continue
    
    if direction == 'forward':
        display.show(Image.ARROW_N)
        motor_right_A.write_digital(1)
        motor_right_B.write_digital(0)
        motor_left_A.write_digital(1)
        motor_left_B.write_digital(0)
    elif direction == 'backward':
        display.show(Image.ARROW_S)
        motor_right_A.write_digital(0)
        motor_right_B.write_digital(1)
        motor_left_A.write_digital(0)
        motor_left_B.write_digital(1)
    elif direction == 'left':
        display.show(Image.ARROW_W)
        motor_right_A.write_digital(0)
        motor_right_B.write_digital(1)
        motor_left_A.write_digital(1)
        motor_left_B.write_digital(0)
    elif direction == 'right':
        display.show(Image.ARROW_E)
        motor_right_A.write_digital(1)
        motor_right_B.write_digital(0)
        motor_left_A.write_digital(0)
        motor_left_B.write_digital(1)
    else:
        display.show(Image.SQUARE)
        motor_right_A.write_digital(0)
        motor_right_B.write_digital(0)
        motor_left_A.write_digital(0)
        motor_left_B.write_digital(0)
    
    sleep(50)