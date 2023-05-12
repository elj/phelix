#!/usr/bin/env python
# -*- coding: utf-8 -*-

#define the different phone modes

currentMode = 0

whichMode = ["phone_on_hook", "dialing", "active_call"]  #0, 1, 2

def get_mode():
    return currentMode

def get_mode_name():
    return whichMode[currentMode]

def set_mode_by_number(i):
    global currentMode
    currentMode = i
    
def set_mode_by_name(n):
    global currentMode
    try:
        i = whichMode.index(n)
        currentMode = i
    except:
        print("invalid mode, not set")