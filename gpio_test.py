import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    crankshaft_value = GPIO.input(18)
    ballpass_value = GPIO.input(23)
    print(crankshaft_value)
    print(ballpass_value)



GPIO.cleanup()
