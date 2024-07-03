#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import phonesound
import phone_modes as modes
import keypad
import voicemail as vm

initial_digits = 7     # default number of digits to check for when starting up


### Functions for logic at each phone branch ##

def dial_tone():
    print("USER: Starting dial tone and listening for digits")
    main_extensions = {"7777777": story_list,
                       "4743549": phelix_main_menu,
                       "9999999": record_test,
                       "0":     phelix_main_menu,
                       "1833284": phelix_debug
                       }
    phonesound.play_dial_tone()
    modes.allow_dialing()
    dialed = ''
    while dialed not in main_extensions: 
        dialed = keypad.accept_keypad_entry_loop(initial_digits, True)
        if modes.on_hook():
            return
        if dialed not in main_extensions:
            print("Not a valid number!") # TODO: Do something to indicate bad number dialed
            phonesound.play_disconnect_with_dial()
    modes.prevent_dialing()
    main_extensions[dialed]()
    print("CR: Ending main dial tone")
    call_reset()

def phelix_debug():
    print("Enter the number to manage")
    modes.allow_dialing()
    dialed = ''
    while dialed not in vm.voicemail_nums:
        dialed = keypad.accept_keypad_entry_loop(7)
        if modes.on_hook():
            return
        elif dialed not in vm.voicemail_nums:
            phonesound.play_ext_msg("no_msg")  
            print("USER: Message not found at that number, try again")
            while phonesound.is_voice_playing():
                if modes.on_hook():
                    return
            phelix_debug()
    modes.prevent_dialing()
    post_listen_msg(dialed)

def call_reset():
    modes.set_mode_by_number(0)
    phonesound.process_hangup()
    keypad.reset_keys_entered()
    #vmrecord.stop_and_delete_voicemail()

### PHELIX STORY OPTIONS ###

def story_list():
    # play the story options list
    phonesound.play_sound_on_voice(phonesound.echo_menu)
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
    modes.prevent_dialing()
    story_ext[dialed](dialed)

    
def play_story(story_num):
    print("USER: Playing story", story_num)
    phonesound.play_story_and_outro(story_num)
    mid_story_ext = {"0": story_list,
                     "1": enter_num_to_leave_msg,
                     "2": post_story
                    }
    modes.allow_dialing()
    dialed = ''
    # TODO: do something different when the story ends?
    while dialed not in mid_story_ext:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    modes.prevent_dialing()
    mid_story_ext[dialed]()

def post_story():
    print("USER: Story over, goodbye")

### CALLING CARD FUNCTIONS ###

def phelix_main_menu(intro="no"):
    print("USER: Do you want to 1-leave a message, 2-hear a message, 3-hear a story?")
    if intro == "yes":
        phonesound.play_sound_on_voice(phonesound.phelix_intro)  # TODO: swap this with just the intro sound
        while phonesound.is_voice_playing():
            if modes.on_hook():
                return
    modes.allow_dialing()
    phonesound.play_sound_on_voice(phonesound.ccmm)  # TODO: swap this with just the instructions
    # ~ while phonesound.is_voice_playing():
        # ~ if modes.on_hook():
            # ~ return
    cc_ext = {"1": enter_num_to_leave_msg,
              "2": retrieve_msg,
              "3": story_list,
              "9": record_test
             }
    dialed = ''
    while dialed not in cc_ext:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    modes.prevent_dialing()
    cc_ext[dialed]()
    
def enter_num_to_leave_msg():
    print("USER: Enter any 7-digit number where you want to leave a message")
    phonesound.play_ext_msg("enter_num")
    modes.allow_dialing()
    dialed = ''
    ### Collect 7 numbers
    ### If it is already in the voicemail_nums list, error and try again
    ### TODO: If it is not in the recorded messages list, proceed to record?
    resolved = False
    while not resolved:
        dialed = keypad.accept_keypad_entry_loop(7)
        if modes.on_hook():
            return
        if dialed in vm.voicemail_nums:
            print("USER: Sorry, try a different number")
            modes.prevent_dialing()
            phonesound.play_sound_on_voice(phonesound.num_taken)
            while phonesound.is_voice_playing():
                if modes.on_hook():
                    return
            enter_num_to_leave_msg()
        else:
            resolved = True
    modes.prevent_dialing()
    record_msg(dialed)
    
def retrieve_msg():
    print("USER: Enter your destination number")
    phonesound.play_ext_msg("retrieve_msg")
    modes.allow_dialing()
    dialed = ''
    while dialed not in vm.voicemail_nums:
        dialed = keypad.accept_keypad_entry_loop(7)
        if modes.on_hook():
            return
        elif dialed not in vm.voicemail_nums:
            phonesound.play_ext_msg("no_msg")  
            print("USER: Message not found at that number, try again")
            while phonesound.is_voice_playing():
                if modes.on_hook():
                    return
            phelix_main_menu()
    modes.prevent_dialing()
    play_requested_msg(dialed)

# ~ def msg_not_found():
    # ~ print("Sorry, that number doesn't have a message")
    # ~ select_msg(0)

def play_requested_msg(num):
    print("USER: Attempting to play the message", num)
    if num in vm.voicemail_nums:
        print("CR: number found")
        time.sleep(0.2)
    # TODO: actually play the message here
    phonesound.play_sound_on_voice(phonesound.beep)
    print("CR: Playing VM intro")
    while phonesound.is_voice_playing():
        if modes.on_hook():
            return
    phonesound.load_and_play_rec(num)
    print("USER: Playing message")
    while phonesound.is_rec_playing():
        if modes.on_hook():
            return
    post_listen_msg(num)

### Do this after playing a requested message
def post_listen_msg(num):
    global post_msg_options_ext
    print("USER: Do you want to 1-listen, 2-save, 3-delete, or 4-rerecord?")
    phonesound.play_ext_msg("post_rec")
    ext_options = post_msg_options_ext
    modes.allow_dialing()
    dialed = ''
    while dialed not in ext_options:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    modes.prevent_dialing()
    ext_options[dialed](num)

### Do all the recording stuff in voicemail
def record_msg(num):
    print("USER: Playing voicemail message...")
    modes.prevent_dialing()
    if phonesound.play_ringing_vm_intro(num) == 0:
        print("CR: Play ringing returned 0")
        return
    #while phonesound.is_voice_playing():
    #    time.sleep(0.1)
    print("USER: Recording test message, press any key when done")
    modes.allow_dialing()
    vm.start_recording(num)
    print("CR: Done with recording stuff, moving on")
    if modes.on_hook():
        return
    modes.prevent_dialing()
    post_rec_msg(num)

def record_test():
    print("Test recording...")
    phonesound.process_hangup()
    vm.start_recording("test_record")
    if modes.on_hook():
        return
    

### Post-recording, always do this
def post_rec_msg(num):
    global post_msg_options_ext
    print("USER: Do you want to 1-listen, 2-save, 3-delete, or 4-rerecord?")
    phonesound.play_ext_msg("post_rec")
    modes.allow_dialing()
    ext_options = post_msg_options_ext
    dialed = ''
    while dialed not in ext_options:
        dialed = keypad.accept_keypad_entry_loop(1)
        if modes.on_hook():
            return
    modes.prevent_dialing()
    if dialed == "3" or dialed == "1":   # (Implicitly) save the message
        vm.add_num_to_vm_list(num)
    ext_options[dialed](num)


### Post-recording menu options

def save_msg(num):
    print("USER: Saving message to list. To hear it again, call back and enter", num)
    phonesound.play_ext_msg("vm_saved")
    while phonesound.is_voice_playing():
        if modes.on_hook():
            return
        time.sleep(0.1)
    phonesound.play_disconnect()
    while phonesound.is_voice_playing():
        if modes.on_hook():
            return
        time.sleep(0.1)
    print("hanging up...")

def delete_msg(num):
    print("USER: Attempting to delete vm at ", num)
    vm.delete_voicemail(num)
    print("USER: You message at", num, "has been deleted. Beep beep beep...")
    phonesound.play_ext_msg("vm_deleted")
    if modes.on_hook():
        return
    while phonesound.is_voice_playing():
        time.sleep(0.1)
    print("hanging up...")


## TODO: Replace with vm function
# ~ def add_num_to_recorded_list(num):
    # ~ global recorded_msgs_ext
    # ~ recorded_msgs_ext[num] = play_msg
    # ~ print("CR: VM list", recorded_msgs_ext)


### Extensions available at more than one branch


post_msg_options_ext = {"2": save_msg,
                        "3": delete_msg,
                        "1": play_requested_msg,
                        "4": record_msg
                        }

# ~ recorded_msgs_ext = {"5751377": play_msg,
                     # ~ "4444444": play_msg,
                     # ~ "5555555": play_msg,
                     # ~ "6666666": play_msg
                     # ~ }

def update_voicemails_list():
    # TODO - update the initial list based on actual files in /recordings
    print("Updating voicemails list - not yet implemented")
    
# def play_welcome_message(ext):
#     phonesound.play_ext_msg(ext)
#     while(phonesound.pygame.mixer.get_busy()):
#             time.sleep(0.1)
#     return
