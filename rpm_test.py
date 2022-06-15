#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import time
import math

rpm = 0
elapse = 0
ball_sensor = 18
sensor = 23
pulse = 0
start_timer = time.time()
balls_dropped = 0

def init_GPIO():				# initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(sensor, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(ball_sensor, GPIO.IN, GPIO.PUD_UP)

def calculate_elapse(channel):			# callback function
    global pulse, start_timer, elapse
    pulse += 1					# increase pulse by 1 whenever interrupt occurred
    elapse = time.time() - start_timer		# elapse for every 1 complete rotation made!
    start_timer = time.time()			# let current time equals to start_timer

def calculate_rpm():
    global pulse, elapse, rpm, start_timer
    if elapse != 0:				# to avoid DivisionByZero error
        rpm = 1/elapse * 10 * 0.7			# Was "* 60", but divided by six to account for 6 encoder wheel tabs/slots
#        rpm = elapse/10
    if time.time()-start_timer > 1:
        rpm = 0
    return rpm

def ball_drop(channel):
    global balls_dropped
    balls_dropped += 1

def init_interrupt():
    GPIO.add_event_detect(sensor, GPIO.FALLING,
                          callback=calculate_elapse, bouncetime=20)
    GPIO.add_event_detect(ball_sensor, GPIO.FALLING,
                          callback=ball_drop, bouncetime=20)

if __name__ == '__main__':
    print("Starting Main")
    init_GPIO()
    init_interrupt()
    while True:
        calculate_rpm()
        print(f"rpm:{round(rpm)}RPM Pulse:{pulse} Balls:{balls_dropped}")
        sleep(0.1)

