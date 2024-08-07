#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os
import sys
import time
import phone_modes as modes

# set number of desired asynchronous channels (referenced later in mixer setup)
number_of_channels = 8
#pygame.print_debug_info()

# look for sound & music files in subfolder 'data'
#pygame.mixer.music.load(os.path.join('data', 'loophole.wav'))#load music
current_folder = os.path.dirname(__file__)
print("sounds folder = ", current_folder)
vm_files = {}

### end custom variables ###
    
### functions and stuff go here ###

def play_dial_tone():
    dialtone.stop()
    dialtone.play(-1)
    
def stop_dial_tone():
    dialtone.fadeout(10)

def set_key_audio(k, desired_state):
    if key_tones.get(k, 0) == 0:
        print("key not found!")
    if(desired_state):
        keys.play(key_tones.get(k), -1)
    else:
        keys.fadeout(10)
        #key_tones.get(k).fadeout(10)

def play_ext_msg(sound_name):  #replace for CallingCard
    sound = ext_audio[sound_name]
    voice.play(sound)

def play_sound_on_voice(sound):
    voice.play(sound)

def play_story_and_outro(story_num):
    voice.play(stories[story_num])
    voice.queue(post_story)

def play_ringing_vm_intro(num):
    voice.play(vm_ring)
    number_sounds = []
    for n in num:
        number_sounds.append(vm_nums[int(n)])        
    if wait_for_playback(voice) == 0:
        return 0
    for n in number_sounds:
        voice.play(n)
        if wait_for_playback(voice) == 0:
            return 0
    voice.play(vm_na)
    if wait_for_playback(voice) == 0:
        return 0

def load_and_play_rec(num):
    print("loading VM files as sounds")
    ## TODO: actually load the files
    rec_filename = num + ".wav"
    rec_sound = pygame.mixer.Sound(os.path.join(current_folder, 'recordings', rec_filename))
    rec.set_source_location(0, 128)
    rec.play(rec_sound)

def wait_for_playback(ch):
    while ch.get_busy():
        if modes.get_mode() == 0:
            return 0
        time.sleep(0.05)

def play_disconnect():
    voice.play(disconnect, -1)

def play_disconnect_with_dial():
    voice.play(disconnect)
    while voice.get_busy():
        time.sleep(0.1)
    voice.play(dialtone, -1)
    
def process_hangup():
    pygame.mixer.stop()

def stop_all():
    pygame.mixer.stop()

def is_voice_playing():
    return voice.get_busy()

def is_rec_playing():
    return rec.get_busy()

def play_welcome_message():  #play immediately after picking up the phone, instead of a dial tone
    print("playing welcome message")
#     welcome_msg.stop()
#     time.sleep(0.3)
#     welcome_msg.play(-1)
    welcome_msg.play(-1)

def stop_welcome_message():
    print("Stopping welcome message")
    #welcome_msg.fadeout(10)

def is_welcome_playing():
    if welcome_msg.get_num_channels() > 0:
        return True
    else:
        return False

### end functions ###
outputs = 2 # Set to 2 by default unless using 4-channel stuff

pygame.mixer.pre_init(44100, -16, outputs, 4096) # setup mixer to avoid sound lag

pygame.init()    #initialize pygame - this is where terrible things happen
pygame.mixer.set_num_channels(number_of_channels)  # must come *after* .init

# set up some test channels
c1 = pygame.mixer.Channel(1)
keys = pygame.mixer.Channel(0)
voice = pygame.mixer.Channel(2)
rec = pygame.mixer.Channel(3)
#c1.set_volume(0.1, 0.9)

# Temp voice files
main_cc = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'CallingCard.wav'))
ccmm = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'CCMM.wav'))
phelix_intro = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', '4-Phelix.wav'))
echo_menu = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'echo_menu.wav'))
story1 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Story1.wav'))
story2 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Story2.wav'))
story3 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Story3.wav'))
story4 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Story4.wav'))
post_story = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Post_story.wav'))
enter_num = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'EnteringMessage.wav'))
retrieve_msg = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Retrieval.wav'))
num_taken = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Already_Taken.wav'))
no_msg = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'no_messages.wav'))
post_rec = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'EndRecording.wav'))
post_listen = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'EndRecording.wav'))
vm_saved = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Saved.wav'))
vm_deleted = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Deleted.wav'))
reached = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Reached.wav'))

# Error for number not found
vm_not_found = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_not_a_working_number.wav'))

ext_audio = {
    "main_cc": main_cc,

    "post_story": post_story,
    "enter_num": enter_num,
    "retrieve_msg": retrieve_msg,
    "num_taken": num_taken,
    "no_msg": no_msg,
    "post_rec": post_rec,
    "post_listen": post_listen,
    "vm_saved": vm_saved,
    "vm_deleted": vm_deleted,
    "reached": reached,
    "vm_intro": reached,
    "vm_not_found": vm_not_found
    }

stories = {
    "1": story1,
    "2": story2,
    "3": story3,
    "4": story4
}


# Key dialing tones
key1s = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-1.wav'))  #load sound
key2s = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-2.wav'))  #load sound
key3s = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-3.wav'))  #load sound
key4s = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-4.wav'))  #load sound
key5s = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-5.wav'))  #load sound
key6s = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-6.wav'))  #load sound
key7s = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-7.wav'))  #load sound
key8s = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-8.wav'))  #load sound
key9s = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-9.wav'))  #load sound
keystars = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-star.wav'))  #load sound
key0s = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-0.wav'))  #load sound
keypounds = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'DTMF-pound.wav'))  #load sound

# Other utility sounds
dialtone = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'dialtone.wav'))
beep = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'keytone4.wav'))
busy_signal = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'busy_tone_loop.wav'))
disconnect = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'disconnect_tones.wav'))

# Numbers spoken by the voicemail lady
vm_0 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_0.wav'))
vm_1 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_1.wav'))
vm_2 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_2.wav'))
vm_3 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_3.wav'))
vm_4 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_4.wav'))
vm_5 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_5.wav'))
vm_6 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_6.wav'))
vm_7 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_7.wav'))
vm_8 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_8.wav'))
vm_9 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_9.wav'))

vm_nums = [vm_0, vm_1, vm_2, vm_3, vm_4, vm_5, vm_6, vm_7, vm_8, vm_9]

# Numbers spoken by Justin
num_0 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'num_0.wav'))
num_1 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'num_1.wav'))
num_2 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'num_2.wav'))
num_3 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'num_3.wav'))
num_4 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'num_4.wav'))
num_5 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'num_5.wav'))
num_6 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'num_6.wav'))
num_7 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'num_7.wav'))
num_8 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'num_8.wav'))
num_9 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'num_9.wav'))

num_nums = [num_0, num_1, num_2, num_3, num_4, num_5, num_6, num_7, num_8, num_9]

# Simulate calling a number to leave a voicemail
vm_ring = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'ringing_answer.wav'))
vm_na = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_is_not_available.wav'))

dialtone.set_volume(0.3)

key_tones = {
    "1": key1s,
    "2": key2s,
    "3": key3s,
    "4": key4s,
    "5": key5s,
    "6": key6s,
    "7": key7s,
    "8": key8s,
    "9": key9s,
    "*": keystars,
    "0": key0s,
    "#": keypounds
}

