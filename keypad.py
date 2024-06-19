#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO
import phone_modes as modes
import phonesound
import call_routing

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio_outputs = [5, 6, 13, 19] #columns - send current out connector B
gpio_inputs = [17, 27, 22] #lines/rows - detect current back connector A

GPIO.setup(gpio_outputs, GPIO.OUT)
GPIO.setup(gpio_inputs, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #use internal pull-down for detecting current

line1 = ["6", "5", "4"]
line2 = ["9", "8", "7"]
line3 = ["#", "0", "*"]
line4 = ["3", "2", "1"]

lines = [line1, line2, line3, line4]

keysEntered = ""    # Track the set of keys entered, as a string

def accept_keypad_entry_loop(d):
    ### collect keys entered until the desired number of keys have been entered
    ### stop if phone hangs up / mode 0
    #print("K: starting keypad loop with", d, "digits")
    reset_keys_entered()

    while len(keysEntered) < d:
        if modes.get_mode() == 1:   #if phone is off the hook and dialing is allowed
            #print("K: detecting keys")
            detectKeys()     # cycle through all GPIO outputs once
        else:   # if phone is on the hook or dialing not allowed
            return
        if keysEntered == "0":
            print("Operator dialed")
            return keysEntered
    print("K: returning total keys entered as", keysEntered)
    thesekeys = keysEntered
    reset_keys_entered()
    return thesekeys


def detectKeys(): # cycle through all the GPIO outputs once and see if any inputs detect signal
    #print("K:starting to detect keys")

    for i in range(len(gpio_outputs)):
        GPIO.output(gpio_outputs[i], GPIO.HIGH)
        #print("testing out of", gpio_outputs[i])
        for j in range(len(gpio_inputs)):
            #print("testing into", j)
            if (GPIO.input(gpio_inputs[j]) == 1):  
                currentKey = lines[i][j]
                #print("detected", currentKey)
                key_pressed(currentKey)
                time.sleep(0.05)
                while GPIO.input(gpio_inputs[j]) == 1:
                    time.sleep(0.05)
                #print(currentKey, "released")
                key_unpressed(currentKey)

        GPIO.output(gpio_outputs[i], GPIO.LOW)
    #print("about to sleep a little")
    #time.sleep(0.1)     # why do? still needed?

anyKeyCurrentlyPressed = 0

def key_pressed(key):
    if anyKeyCurrentlyPressed == 1:
        return
    else:
        set_whether_any_key_pressed(1)
        #print(key, "pressed")
        phonesound.stop_dial_tone() 	# stop the dial tone or welcome message if any key is pressed
        phonesound.stop_welcome_message()	# TODO: maybe make a global stop for anything that isn't a key sound?
        phonesound.set_key_audio(key, 1)
    
def key_unpressed(key):
    set_whether_any_key_pressed(0)
    #print(key, "unpressed")
    add_to_keys_entered(key)
    phonesound.set_key_audio(key, 0)
    
    
def set_whether_any_key_pressed(state):
    global anyKeyCurrentlyPressed
    if (state == 1):
        anyKeyCurrentlyPressed = 1
    elif (state == 0):
        anyKeyCurrentlyPressed = 0
    else:
        print("bad key press state received")
        
def add_to_keys_entered(k):
    global keysEntered
    keysEntered = keysEntered + k
    print("Entered", keysEntered)
        
def reset_keys_entered():
    global keysEntered
    keysEntered = ""

        
