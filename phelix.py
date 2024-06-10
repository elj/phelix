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
    global call_start, call_end
    #print("hook state changed")
    if GPIO.input(channel) == 0:
        print("Phone ON hook")
        modes.set_mode_by_number(0)
        phonesound.process_hangup()
        keypad.reset_keys_entered()
        vmrecord.stop_recording_voicemail()

    else:
        print("this Phone is OFF the hook")
        phonesound.stop_welcome_message()   # TODO: should probably stop any other audio here, too
        vmrecord.reset_vmStop()


GPIO.add_event_detect(gpio_hook, GPIO.BOTH, callback=phone_hook_callback, bouncetime=1)

def start_loop():
    phonesound.play_welcome_message()
    while phonesound.is_welcome_playing():
        time.sleep(0.01)
    print("PH: it stopped playing")


def main(args):
    print("starting Phelix, ready!")
    # keep running while waiting for input
    # when phone is off the hook, start the simulation
    # when phone is back on the hook, end the simulation but keep running

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

