#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import phonesound
import vmrecord
import phone_modes as modes
import keypad


initial_digits = 5     # default number of digits to check for when starting up


### Functions for logic at each phone branch ##

def dial_tone():
    print("USER: Starting dial tone and listening for digits")
    main_extensions = {"18007": story_list,
                       "18002": calling_card
                       # "18003": debug
                       }
    phonesound.play_dial_tone()
    modes.allow_dialing()
    dialed = ''
    while dialed not in main_extensions: ### FIGURE OUT LOOP HERE - collect sets of digits until an extension match is found
        dialed = keypad.accept_keypad_entry_loop(initial_digits)
        if modes.on_hook():
            return
        #time.sleep(0.05)
    main_extensions[dialed]()

def story_list():
    # play the story options list
    story_ext = {"1": play_story,
                 "2": play_story,
                 "3": play_story,
                 "4": play_story
                 }
    print("USER: Pick 1 2 3 or 4 to hear that story, or 0 at any time")
    modes.allow_dialing()
    dialed = ''
    #print("CR: starting while loop in story list")
    while dialed not in story_ext:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
        #time.sleep(0.05)
    run = story_ext[dialed](dialed)
    # listen for key press
    
def play_story(story):
    print("USER: Playing story", story)
    mid_story_ext = {"0": story_list
                    }
    modes.allow_dialing()
    dialed = ''
    while dialed not in mid_story_ext:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    run = mid_story_ext[dialed]()

def calling_card():
    print("USER: Do you want to 1-leave a message or 2-hear a message?")
    cc_ext = {"1": new_msg,
              "2": select_msg
             }
    modes.allow_dialing()
    dialed = ''
    while dialed not in cc_ext:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    run = cc_ext[dialed]()
    
def new_msg():
    print("USER: Enter any 7-digit number where you want to leave a message")
    modes.allow_dialing()
    dialed = ''
    ### Collect 7 numbers
    ### If it is already in the recorded_msgs_ext list, error and try again
    ### If it is not in the recorded messages list, proceed to record
    resolved = False
    while not resolved:
        dialed = keypad.accept_keypad_entry_loop(7)
        if modes.on_hook():
            return
        if dialed in recorded_msgs_ext:
            print("USER: Sorry, try a different number")
        else:
            resolved = True
    record_msg(dialed)
    
def select_msg():
    print("USER: Enter your destination number")
    modes.allow_dialing()
    dialed = ''
    while dialed not in recorded_msgs_ext:
        dialed = keypad.accept_keypad_entry_loop(7)
        if modes.on_hook():
            return
        elif dialed not in recorded_msgs_ext:
            print("USER: Message not found at that number, try again")
    run = recorded_msgs_ext[dialed](dialed)

# ~ def msg_not_found():
    # ~ print("Sorry, that number doesn't have a message")
    # ~ select_msg(0)

def play_msg(num):
    print("USER: Playing message", num)
    if modes.on_hook():
        return
    post_listen_msg(num)

def post_listen_msg(num):
    global post_msg_options_ext
    print("USER: Do you want to 1-save, 2-delete, 3-listen, or 4-rerecord?")
    ext_options = post_msg_options_ext
    dialed = ''
    while dialed not in ext_options:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    run = ext_options[dialed](num)

def record_msg(num):
    print("USER: Recording message at", num, "press any key when you're done")
    # TODO: Actually record, possibly re-recording/re-writing to file
    dialed = 'a'
    while dialed == "a":
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    # stop recording
    post_listen_msg(num)
    
def post_rec_msg(num):
    global post_msg_options_ext
    print("USER: Do you want to 1-save, 2-delete, 3-listen, or 4-rerecord?")
    ext_options = post_msg_options_ext
    dialed = ''
    while dialed not in ext_options:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    run = ext_options[dialed](num)

def save_msg(num):
    print("USER: Saving message to list. To hear it again, call back and enter", num)
    # TODO: any actual stuff for saving the file
    add_num_to_recorded_list(num)
    if modes.on_hook():
        return
    time.sleep(2)
    print("hanging up...")

def delete_msg(num):
    global recorded_msgs_ext
    print("USER: You message has been deleted. Beep beep beep...")
    # TODO: Actually delete file if it exists
    if num in recorded_msgs_ext:
        recorded_msgs_ext.pop(num)
    if modes.on_hook():
        return
    time.sleep(2)
    print("hanging up...")

def listen_to_msg(num):
    add_num_to_recorded_list(num)
    # TODO: anything to actually save the recorded file
    if modes.on_hook():
        return
    play_msg(num)

def add_num_to_recorded_list(num):
    global recorded_msgs_ext
    recorded_msgs_ext[num] = play_msg


### Allowable extensions to dial for each branch TODO: finish moving these to their functions


post_msg_options_ext = {"1": save_msg,
                        "2": delete_msg,
                        "3": listen_to_msg,
                        "4": record_msg
                        }

recorded_msgs_ext = {"1111111": play_msg,
                     "1234567": play_msg
                     }

    
# def play_welcome_message(ext):
#     phonesound.play_ext_msg(ext)
#     while(phonesound.pygame.mixer.get_busy()):
#             time.sleep(0.1)
#     return
