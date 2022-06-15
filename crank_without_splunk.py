#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import time
import math
import pygame

from pygame.locals import (
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.mouse.set_visible(False)

# pygame.freetype.init()
display_width = 1280
display_height = 800

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (128, 128, 128)

counterDisplay = pygame.display.set_mode((display_width, display_height))

red_background_image = pygame.image.load("/home/pi/Crank/red.png").convert()
blue_background_image = pygame.image.load("/home/pi/Crank/blue.png").convert()

gilroy_location = '/home/pi/Crank/Gilroy-Bold.ttf'
gilsans_location = '/home/pi/Crank/GillSans-Bold.ttf'

current_background = red_background_image
text_color = white
current_font = gilroy_location

counterDisplay.blit(current_background, [0, 0])
pygame.display.set_caption('Crank Counter')
clock = pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, text_color)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font(current_font, 350)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    counterDisplay.blit(current_background, [0, 0])
    counterDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


#def rpm_display(number):
#    text = f"{number} RPM"
#    largeText = pygame.font.Font(current_font, 300)
#    TextSurf, TextRect = text_objects(text, largeText)
#    TextRect.center = ((display_width/2), ((display_height/3) + 70))
#    counterDisplay.blit(current_background, [0, 0])
#    counterDisplay.blit(TextSurf, TextRect)
#    pygame.display.update()


#def balls_display(number):
#    text = f"{number} Balls"
#    largeText = pygame.font.Font(current_font, 300)
#    TextSurf, TextRect = text_objects(text, largeText)
#    TextRect.center = ((display_width/2), ((2*(display_height/3)) + 70))
#    counterDisplay.blit(current_background, [0, 0])
#    counterDisplay.blit(TextSurf, TextRect)
#    pygame.display.update()


def display_stats(rev, balls):
    rpm_str = f"{rev} RPM"
    ball_str = f"{balls} Balls"
    rpm_text = pygame.font.Font(current_font, 280)
    rpm_surf, rpm_rect = text_objects(rpm_str, rpm_text)
    rpm_rect.center = ((display_width/2), ((display_height/3) + 0))
    if (len(ball_str) < 10):
        ball_text = pygame.font.Font(current_font, 280)
    elif (len(ball_str) == 10):
        ball_text = pygame.font.Font(current_font, 240)
    elif (len(ball_str) == 11):
        ball_text = pygame.font.Font(current_font, 200)
    else:
        ball_text = pygame.font.Font(current_font, 100)
    ball_surf, ball_rect = text_objects(ball_str, ball_text)
    ball_rect.center = ((display_width/2), ((2*(display_height/3)) + 70))
    counterDisplay.blit(current_background, [0, 0])
    counterDisplay.blit(rpm_surf, rpm_rect)
    counterDisplay.blit(ball_surf, ball_rect)
    pygame.display.update()


rpm = 0
last_rpm = 0
elapse = 0
ball_sensor = 18
sensor = 23
pulse = 0
start_timer = time.time()
balls_dropped = 0
last_balls_dropped = 0


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
        # Was "* 60", but div by six 'cause 6 encoder wheel tabs, mult by 0.7 for pulley dif
        rpm = round(1/elapse * 10 * 0.7)
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


#message_display("CRaNK!")
display_stats(0,0)

init_GPIO()
init_interrupt()

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:   # Did the user hit a key?
            if event.key == K_2:
                current_background = blue_background_image
                message_display("Crank!")
            if event.key == K_3:
                current_background = red_background_image
                message_display("Crank!")
            if event.key == K_4:
                text_color = white
                message_display("Crank!")
            if event.key == K_5:
                text_color = black
                message_display("Crank!")
            if event.key == K_6:
                text_color = red
                message_display("Crank!")
            if event.key == K_7:
                current_font = gilroy_location
                message_display("Crank!")
            if event.key == K_8:
                current_font = gilsans_location
                message_display("Crank!")
            elif event.key == K_ESCAPE:
                running = False
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

    calculate_rpm()
    if rpm != last_rpm:
        display_stats(rpm, balls_dropped)
        last_rpm = rpm
    if balls_dropped != last_balls_dropped:
        display_stats(rpm, balls_dropped)
        last_balls_dropped = balls_dropped
    #print(f"rpm:{round(rpm)}RPM Pulse:{pulse} Balls:{balls_dropped}")
    sleep(0.05)
