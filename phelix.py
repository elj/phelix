#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import pygame
import phonesound
import call_routing
#import keypad
import phone_modes as modes
import voicemail as vm

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio_hook = 18

GPIO.setup(gpio_hook, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def phone_hook_callback(channel):
    global call_start, call_end
    #print("hook state changed")
    if GPIO.input(channel) == 0:
        print("Phone ON hook")
        call_routing.call_reset()
    else:
        print("this Phone is OFF the hook")
        modes.allow_dialing()


GPIO.add_event_detect(gpio_hook, GPIO.BOTH, callback=phone_hook_callback, bouncetime=1)



def main(args):
    print("starting Phelix, ready!")
    # keep running while waiting for input
    # when phone is off the hook, start the simulation
    # when phone is back on the hook, end the simulation but keep running

    ## TODO: load VM files here
    vm.read_initial_vm_files()

    try:
        while True:
            if GPIO.input(gpio_hook) == 1:
                print("PH: starting dial tone")
                call_routing.dial_tone()
                time.sleep(0.1)
            else:
                #print("PH: phone on hook")
                time.sleep(0.1)

        print("PH: finished the first loop I started")
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("PH: Exiting with cleanup")

    print("PH: The end")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

