#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import pygame
import phonesound

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio_outputs = [18, 23, 24, 25] #columns
gpio_inputs = [16, 20, 21] #lines/rows

GPIO.setup(gpio_outputs, GPIO.OUT)
GPIO.setup(gpio_inputs, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

anyButton = 0

def gpio_change_callback(channel):
    global anyButton
    if (channel == 0):
        print("Not a door!")
        return
    time.sleep(0.1)
    if GPIO.input(channel):
        #print("Button pressed", channel)
        anyButton = 1
        #doorsound.set_door_audio(door, True)
    else:
        #print("Button released", channel)
        for i in range(len(gpio_outputs)):
            GPIO.output(gpio_outputs[i], GPIO.LOW) #TODO: make this more elegant
        anyButton = 0
        #doorsound.set_door_audio(door, False)

for i in gpio_inputs:
    GPIO.add_event_detect(i, GPIO.BOTH, callback=gpio_change_callback, bouncetime=100)
    gpio_change_callback(i)

line2 = ["9", "8", "7"]
line3 = ["6", "5", "4"]
line4 = ["3", "2", "1"]
line1 = ["#", "0", "*"]
lines = [line1, line2, line3, line4]

def readKey():
    global anyButton
    for i in range(len(gpio_outputs)):
        GPIO.output(gpio_outputs[i], GPIO.HIGH)
        #print("testing ", gpio_outputs[i])
        for j in range(len(gpio_inputs)):
            if anyButton == 0:
                if(GPIO.input(gpio_inputs[j]) == 1):
                    print(lines[i][j])
                    time.sleep(0.3)
                    return
            else:
                return
        GPIO.output(gpio_outputs[i], GPIO.LOW)
    time.sleep(0.1)
    #print("anyButton=", anyButton)
            

def main(args):
    print("reading keys...")
    try:
        while True:
            if anyButton == 0:
                readKey()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("The end")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
