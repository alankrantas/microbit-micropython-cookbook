# Simple micro:bit V2 remote control car

Since the micro:bit V2 can output 300 mA instead of 90 mA from its 3V pin, you can actually build a motor car with a simple breakout, a L9110S H-bridge motor driver board and a generic, small 5V USB power bank.

This RC car needs another micro:bit (it can be either V1 or V2) as the remote controller.

### Required hardware

* 2 BBC micro:bit V2 (or one V2 and one V1)
* a L9110s driver board
* a cheap 2WD robot car chassis
* a small 5V USB powerbank

### Wiring

| L9110S | micro:bit V2 |
| --- | --- |
| B-1A | P1 |
| B-1B | P2 |
| GND | GND |
| VCC | 3V |
| A-1A | P8 |
| A-1B | P12 |

And connect your power bank to the micro:bit V2's USB port.

Be noted that many power banks shut themselves off when there are not enough current draw, which would happen when both motors are not running for a few seconds. You can try to turn on the "always on mode" or buy one of those cheap ones that don't shut off.

If you have a micro:bit extension board that offer 5V output (either from USB connection or on-board batteries), a micro:bit V1 can be used on the car as well. Simply connect the VCC pin to the 5V pin.

![1](https://github.com/alankrantas/microbit-micropython-cookbook/blob/master/rc_car/rc_car.png)

### Upload code

Copy the content of following MicroPython code into the [official Python editor](https://python.microbit.org/v/2), connect the board and flash it:

* [Controller](https://github.com/alankrantas/microbit-micropython-cookbook/blob/master/rc_car/rc_controller.py) (to the V2 on the car)
* [Car](https://github.com/alankrantas/microbit-micropython-cookbook/blob/master/rc_car/rc_car.py) (to a V2 or V1)

In both scripts the ```RADIO_CHANNEL``` variable defines the radio channel shared between the controller and the car. Change it if you are going to operate near other people also using micro:bit's radio functions.

### Control

Tilt the controller to different directions. Direction arraws would show on both the controller and the car.

The controller can be connected to any USB or battery power.
