#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pygame
import phone_modes as modes
import phonesound
import call_routing

anyKeyCurrentlyPressed = 0
keysEntered = ""

#keyCode = "123"

dialed_ext = ""

def key_pressed(key):
    if anyKeyCurrentlyPressed == 1:
        return
    else:
        set_whether_any_key_pressed(1)
        print(key, "pressed")
        add_to_keys_entered(key)
        phonesound.set_key_audio(key, 1)
    
def key_unpressed(key):
    set_whether_any_key_pressed(0)
    print(key, "unpressed")
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
    print(keysEntered)
        
def reset_keys_entered():
    global keysEntered
    keysEntered = ""
    
def check_for_code_match():
    if keysEntered in call_routing.extensions: # change to: any 5-digit number
        print("match detected!")
        modes.set_mode_by_number(2)
        set_dialed_extension(keysEntered)
        call_routing.process_call(dialed_ext)
        #phonesound.play_voicemail()
    return

def set_dialed_extension(ext):
    global dialed_ext
    dialed_ext = ext
    print("You dialed:", dialed_ext)
    reset_keys_entered()
        