#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import pygame
import phonesound
import call_routing
import keypad
import phone_modes as modes
import vmrecord

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio_hook = 18

GPIO.setup(gpio_hook, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def phone_hook_callback(channel):
    #print("hook state changed")
    if GPIO.input(channel) == 0:
        print("Phone ON hook")
        #start_loop()
        modes.set_mode_by_number(0)
        phonesound.process_hangup()
        keypad.reset_keys_entered()
        call_routing.reset_digits()
        call_routing.reset_ext()
        vmrecord.stop_recording_voicemail()
        #keypad.accept_keypad_entry_loop(0)
        
    else:
        print("this Phone is OFF the hook")
        modes.allow_dialing()
        phonesound.stop_welcome_message()   # TODO: should probably stop any other audio here, too
        phonesound.play_dial_tone()
        #phonesound.play_welcome_message() # can use dial tone or welcome message, also adjust stop below
        vmrecord.reset_vmStop()


GPIO.add_event_detect(gpio_hook, GPIO.BOTH, callback=phone_hook_callback, bouncetime=1)

def start_loop():
    phonesound.play_welcome_message()
    while phonesound.is_welcome_playing():
        time.sleep(0.01)
    print("PH: it stopped playing")


def main(args):
    print("starting Phelix")
    
    try:
        #start_loop()
        #keypad.accept_keypad_entry_loop()
        
        while True:
            #print("K: Mode is", modes.get_mode())
            if (modes.get_mode() == 1):   #if phone is off the hook and call is not started
                #print("K: detecting keys")
                detected = keypad.detectKeys()     # cycle through GPIO outputs one at a time
                if detected:
                    call_routing.check_for_ext_match()
            elif (modes.get_mode() == 2):
                print("K: mode is 2")
                detectKeys()    # why do?
            
        print("PH: finished the first loop I started")
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("PH: The end")
        
    print("PH: about to end")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

