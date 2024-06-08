#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import phonesound
import vmrecord
import phone_modes as modes
import keypad


### Functions for detecting whether an extension was dialed or not

dialed_ext = ""
digits = 5     # default number of digits to check for when starting up

def set_dialed_ext(ext):
    global dialed_ext
    dialed_ext = ext
    print("CR: You dialed:", dialed_ext)
    keypad.reset_keys_entered()
    
def reset_digits():
    global digits
    digits = 5
    
def set_digits(d):
    global digits
    digits = d


### Functions for logic at each phone branch ##

def dial_tone():
    print("USER: Starting dial tone and listening for digits")
    main_extensions = {"18007": story_list,
                       "18002": calling_card
                       # "18003": debug
                       }
    phonesound.play_dial_tone()
    set_available_ext_list(main_extensions)
    modes.allow_dialing()
    dialed = ''
    while dialed not in main_extensions: ### FIGURE OUT LOOP HERE - collect sets of digits until an extension match is found
        dialed = keypad.accept_keypad_entry_loop(digits)
        if modes.on_hook():
            return
        #time.sleep(0.05)
    run = main_extensions[dialed]()

def story_list():
    # play the story options list
    story_ext = {"1": play_story,
                 "2": play_story,
                 "3": play_story,
                 "4": play_story
                 }
    print("USER: Pick 1 2 3 or 4 to hear that story")
    set_available_ext_list(story_ext)
    modes.allow_dialing()
    dialed = ''
    print("CR: starting while loop in story list")
    while dialed not in story_ext:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
        #time.sleep(0.05)
    run = story_ext[dialed](dialed)
    # listen for key press
    
def play_story(story):
    print("Playing story", story)
    mid_story_ext = {"0": story_list
                    }
    set_available_ext_list(mid_story_ext)
    modes.allow_dialing()
    dialed = ''
    while dialed not in mid_story_ext:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    run = mid_story_ext[dialed]()

def calling_card():
    print("Do you want to 1 leave a message or 2 hear a message?")
    # ~ cc_ext = {"1": new_msg,
              # ~ "2": select_msg
             # ~ }
    # ~ set_available_ext_list(cc_ext)
    # ~ modes.allow_dialing()
    # ~ dialed = ''
    # ~ keypad.accept_keypad_entry_loop()
    
# ~ def new_msg(ext):
    # ~ print("Enter any 7-digit number")
    # ~ modes.allow_dialing()
    # ~ keypad.accept_keypad_entry_loop()
    
# ~ def select_msg(ext):
    # ~ print("Enter your destination number")
    # ~ set_available_ext_list(recorded_msgs_ext)
    # ~ modes.allow_dialing()
    # ~ keypad.accept_keypad_entry_loop()
    
# ~ def msg_not_found():
    # ~ print("Sorry, that number doesn't have a message")
    # ~ select_msg(0)
    
    
def play_msg(num):
    print("Playing message", num)
    calling_card(0)
    


### Allowable extensions to dial for each branch TODO: finish moving these to their functions
    


story_ext = {"1": play_story,
             "2": play_story,
             "3": play_story,
             "4": play_story
             }

# 
# rec_options_ext = {"1": save_msg,
#                    "2": delete_msg,
#                    "3": listen_to_msg,
#                    "4": rerecord_msg
#                    }

recorded_msgs_ext = {"1111111": play_msg,
                     "1234567": play_msg
                     }

avail_ext = ''

### Functions to manage the available extensions list

def set_available_ext_list(ext_list):
    global avail_ext
    avail_ext = ext_list
    
def reset_ext():
    global avail_ext
    avail_ext = ''
    
    
# def play_welcome_message(ext):
#     phonesound.play_ext_msg(ext)
#     while(phonesound.pygame.mixer.get_busy()):
#             time.sleep(0.1)
#     return
