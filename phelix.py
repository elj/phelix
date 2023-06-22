#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import pygame
import phonesound
import keypad
import phone_modes as modes
import vmrecord

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio_outputs = [5, 6, 13, 19] #columns - send current out connector B
gpio_inputs = [17, 27, 22] #lines/rows - detect current back connector A
gpio_hook = 18

GPIO.setup(gpio_outputs, GPIO.OUT)
GPIO.setup(gpio_inputs, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #use internal pull-down for detecting current
GPIO.setup(gpio_hook, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

line1 = ["6", "5", "4"]
line2 = ["9", "8", "7"]
line3 = ["#", "0", "*"]
line4 = ["3", "2", "1"]

lines = [line1, line2, line3, line4]

def gpio_change_callback(channel):
    if (channel == 0):
        print("Unknown GPIO input!")
        return
    if GPIO.input(channel): #if a key was pressed indicate which of the 3 inputs detected it
        print("GPIO", channel, "closed")
        return
    else:                   #if a key was released indicate which of the 3 inputs detected it
        print("GPIO", channel, "open")
        # TODO: figure out a way to use keypad.key_unpressed here?
        for i in range(len(gpio_outputs)):  #set all 4 GPIO outputs to off
            GPIO.output(gpio_outputs[i], GPIO.LOW) #TODO: just set the currently active one off


def phone_hook_callback(channel):
    #print("hook state changed")
    if GPIO.input(channel) == 0:
        print("Phone ON hook")
        modes.set_mode_by_number(0)
        phonesound.process_hangup()
        keypad.reset_keys_entered()
        vmrecord.stop_recording_voicemail()
    else:
        print("this Phone is OFF the hook")
        modes.set_mode_by_number(1)
        #phonesound.play_dial_tone()
        phonesound.play_welcome_message()
        vmrecord.reset_vmStop()


GPIO.add_event_detect(gpio_hook, GPIO.BOTH, callback=phone_hook_callback, bouncetime=1)

#for i in gpio_inputs:  # for each GPIO input, call a function with the channel number
#     GPIO.add_event_detect(i, GPIO.BOTH, callback=gpio_change_callback, bouncetime=10)
#     gpio_change_callback(i) # also get the current state when starting the program
#phone_hook_callback(gpio_hook)



def detectKeys(): # cycle through GPIO outputs and see if any inputs detect signal
    for i in range(len(gpio_outputs)):
        GPIO.output(gpio_outputs[i], GPIO.HIGH)
        #print("testing out of", gpio_outputs[i])
        for j in range(len(gpio_inputs)):
            #print("testing into", j)
            if (GPIO.input(gpio_inputs[j]) == 1):
                #phonesound.stop_dial_tone()
                phonesound.stop_welcome_message()
                currentKey = lines[i][j]
                print("detected", currentKey)
                keypad.key_pressed(currentKey)
                time.sleep(0.1)
                while GPIO.input(gpio_inputs[j]) == 1:
                    time.sleep(0.05)
                #print(currentKey, "released")
                keypad.key_unpressed(currentKey)
        GPIO.output(gpio_outputs[i], GPIO.LOW)
    time.sleep(0.1)
    #print("anyButton=", anyButton)
            

def main(args):
    print("starting Phelix")
    
    try:
        while True:
            if (modes.get_mode() == 1):   #if phone is off the hook and call is not started
                detectKeys()     # cycle through GPIO outputs one at a time
                keypad.check_for_code_match()
            elif (modes.get_mode() == 2):
                detectKeys()
            else:             
                time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("The end")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

