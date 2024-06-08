#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import phonesound
import vmrecord
import phone_modes as modes
import keypad


### Functions for detecting whether an extension was dialed or not

dialed_ext = ""
digits = 10     # default number of digits to check for when starting up

def check_for_ext_match():
    global digits
    #print("CR: checking for match")
    if keypad.keysEntered in avail_ext: 
        print("CR: match detected!")
        modes.set_mode_by_number(2)
        set_dialed_ext(keypad.keysEntered)
        #try:
        run = avail_ext[dialed_ext](dialed_ext)
    if len(keypad.keysEntered) >= digits:
        print("CR: resetting keys")
        keypad.reset_keys_entered()
        

def check_for_digit_match():
    if keypad.keysEntered in avail_ext: 
        print("CR: match detected!")
        modes.set_mode_by_number(2)
        set_dialed_ext(keypad.keysEntered)
        run = avail_ext[dialed_ext](dialed_ext)
    else:
        # TODO: do something useful if they dialed a wrong number?
        keypad.reset_keys_entered()
        #phonesound.play_voicemail()

def set_dialed_ext(ext):
    global dialed_ext
    dialed_ext = ext
    print("CR: You dialed:", dialed_ext)
    keypad.reset_keys_entered()
    
def reset_digits():
    global digits
    digits = 10
    
def set_digits(d):
    global digits
    digits = d


### Functions for logic at each phone branch ##
    
def process_initial_call(ext):
    print("Processing call to", ext)
    time.sleep(1)
    run = main_extensions[ext]()
    return

def story_list(ext):
    # play the story options list
    print("Pick 1 2 3 or 4 to hear that story")
    set_available_ext_list(story_ext)
    modes.allow_dialing()
    set_digits(1)
    keypad.accept_keypad_entry_loop()
    # listen for key press
    
def play_story(story):
    print("Playing story", story)
    set_available_ext_list(mid_story_ext)
    modes.allow_dialing()
    set_digits(1)
    keypad.accept_keypad_entry_loop()

def calling_card(ext):
    print("Do you want to 1 leave a message or 2 hear a message?")
    set_available_ext_list(cc_ext)
    modes.allow_dialing()
    keypad.accept_keypad_entry_loop()
    
def new_msg(ext):
    print("Enter any 7-digit number")
    modes.allow_dialing()
    set_digits(7)
    keypad.accept_keypad_entry_loop()
    
def select_msg(ext):
    print("Enter your destination number")
    set_available_ext_list(recorded_msgs_ext)
    modes.allow_dialing()
    keypad.accept_keypad_entry_loop()
    
def msg_not_found():
    print("Sorry, that number doesn't have a message")
    select_msg(0)
    
    
def play_msg(num):
    print("Playing message", num)
    calling_card(0)
    


### Allowable extensions to dial for each branch
    
main_extensions = {"18007": story_list,
                   "18002": calling_card
                   # "18003": debug
                   }

story_ext = {"1": play_story,
             "2": play_story,
             "3": play_story,
             "4": play_story
             }

mid_story_ext = {"0": story_list}

cc_ext = {"1": new_msg,
          "2": select_msg
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

avail_ext = main_extensions

### Functions to manage the available extensions list

def set_available_ext_list(ext_list):
    global avail_ext
    avail_ext = ext_list
    
def reset_ext():
    global avail_ext, main_extensions
    avail_ext = main_extensions
    
    
# def play_welcome_message(ext):
#     phonesound.play_ext_msg(ext)
#     while(phonesound.pygame.mixer.get_busy()):
#             time.sleep(0.1)
#     return
