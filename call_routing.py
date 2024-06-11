#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import phonesound
import phone_modes as modes
import keypad
import voicemail as vm

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
    print("CR: Ending main dial tone")
    call_reset()

def call_reset():
    modes.set_mode_by_number(0)
    phonesound.process_hangup()
    keypad.reset_keys_entered()
    #vmrecord.stop_and_delete_voicemail()

### PHELIX STORY OPTIONS ###

def story_list():
    # play the story options list
    phonesound.play_ext_msg("main_phelix")
    story_ext = {"1": play_story,
                 "2": play_story,
                 "3": play_story,
                 "4": play_story
                 }
    print("USER: Pick 1 2 3 or 4 to hear that story")
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
    
def play_story(story_num):
    print("USER: Playing story", story_num)
    story_sound = "story" + story_num
    phonesound.play_ext_msg(story_sound)
    mid_story_ext = {"0": story_list,
                     "1": leave_msg,
                     "2": post_story
                    }
    modes.allow_dialing()
    dialed = ''
    # TODO: do something different when the story ends?
    while dialed not in mid_story_ext:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    run = mid_story_ext[dialed]()

def post_story():
    print("USER: Story over, goodbye")

### CALLING CARD FUNCTIONS ###

def calling_card():
    print("USER: Do you want to 1-leave a message or 2-hear a message?")
    phonesound.play_ext_msg("main_cc")
    cc_ext = {"1": enter_num_to_leave_msg,
              "2": retrieve_msg
             }
    modes.allow_dialing()
    dialed = ''
    while dialed not in cc_ext:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    cc_ext[dialed]()
    
def enter_num_to_leave_msg():
    print("USER: Enter any 7-digit number where you want to leave a message")
    phonesound.play_ext_msg("enter_num")
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
    
def retrieve_msg():
    print("USER: Enter your destination number")
    phonesound.play_ext_msg("retrieve_msg")
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
    phonesound.play_ext_msg("post_story")
    ext_options = post_msg_options_ext
    dialed = ''
    while dialed not in ext_options:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    run = ext_options[dialed](num)

### Do all the recording stuff in voicemail
def record_msg(num):
    print("USER: Playing voicemail message...")
    phonesound.play_ext_msg("reached")
    while phonesound.is_voice_playing():
        time.sleep(0.1)
    print("USER: Recording test message, press any key when done")
    vm.start_recording(num)
    print("CR: Done with recording stuff, moving on")
    post_rec_msg(num)
    
def post_rec_msg(num):
    global post_msg_options_ext
    print("USER: Do you want to 1-save, 2-delete, 3-listen, or 4-rerecord?")
    phonesound.play_ext_msg("post_rec")
    modes.allow_dialing()
    ext_options = post_msg_options_ext
    dialed = ''
    while dialed not in ext_options:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    run = ext_options[dialed](num)

def save_msg(num):
    print("USER: Saving message to list. To hear it again, call back and enter", num)
    phonesound.play_ext_msg("vm_saved")
    add_num_to_recorded_list(num)
    if modes.on_hook():
        return
    while phonesound.is_voice_playing():
        time.sleep(0.1)
    print("hanging up...")

def delete_msg(num):
    global recorded_msgs_ext
    # TODO: Actually delete file if it exists
    if num in recorded_msgs_ext:
        recorded_msgs_ext.pop(num)
    vm.delete_voicemail(num)
    print("USER: You message at", num, "has been deleted. Beep beep beep...")
    phonesound.play_ext_msg("vm_deleted")
    if modes.on_hook():
        return
    while phonesound.is_voice_playing():
        time.sleep(0.1)
    print("hanging up...")

def listen_to_msg(num):
    # TODO: Fix this so it doesn't keep adding to the list
    add_num_to_recorded_list(num)
    if modes.on_hook():
        return
    play_msg(num)

def add_num_to_recorded_list(num):
    global recorded_msgs_ext
    recorded_msgs_ext[num] = play_msg


### Extensions available at more than one branch


post_msg_options_ext = {"1": save_msg,
                        "2": delete_msg,
                        "3": listen_to_msg,
                        "4": record_msg
                        }

recorded_msgs_ext = {"5751377": play_msg,
                     "4444444": play_msg,
                     "5555555": play_msg,
                     "6666666": play_msg
                     }

def update_voicemails_list():
    # TODO - update the initial list based on actual files in /recordings
    print("Updating voicemails list - not yet implemented")
    
# def play_welcome_message(ext):
#     phonesound.play_ext_msg(ext)
#     while(phonesound.pygame.mixer.get_busy()):
#             time.sleep(0.1)
#     return
