#!/usr/bin/env python
# -*- coding: utf-8 -*-

#define the different phone modes

currentMode = 0

whichMode = ["phone_on_hook", "dialing_accepted", "no_dialing"]  #0, 1, 2

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
        
def allow_dialing():
    global currentMode
    currentMode = 1

def prevent_dialing():
    global currentMode
    currentMode = 2

def on_hook():
    if currentMode == 0:
        return True
    else:
        return False

def no_dialing():
    if currentMode == 2:
        return True
    else:
        return False
