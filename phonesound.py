#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os
import sys
import time
import phone_modes as modes

# set number of desired asynchronous channels (referenced later in mixer setup)
number_of_channels = 8

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
            return
    voice.play(vm_na)
    if wait_for_playback(voice) == 0:
        return 0

def load_and_play_rec(num):
    print("loading VM files as sounds")
    ## TODO: actually load the files
    rec_filename = num + ".wav"
    rec_sound = pygame.mixer.Sound(os.path.join(current_folder, 'recordings', rec_filename))
    rec.play(rec_sound)

def wait_for_playback(ch):
    while ch.get_busy():
        if modes.get_mode() == 0:
            return 0
        time.sleep(0.05)
    
def process_hangup():
    pygame.mixer.stop()
    
def play_waymark():
    waymark.play()

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
    welcome_msg.fadeout(10)

def is_welcome_playing():
    if welcome_msg.get_num_channels() > 0:
        return True
    else:
        return False

### end functions ###

pygame.mixer.pre_init(44100, -16, 6, 4096) # setup mixer to avoid sound lag

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
main_phelix = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'MainNumber.wav'))
story1 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Story1.wav'))
story2 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Story2.wav'))
story3 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Story3.wav'))
story4 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Story4.wav'))
post_story = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'LeaveMessage.wav'))
enter_num = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'EnteringMessage.wav'))
retrieve_msg = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Retrieval.wav'))
no_msg = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'NoMessage.wav'))
post_rec = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'EndRecording.wav'))
post_listen = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'EndRecording.wav'))
vm_saved = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Saved.wav'))
vm_deleted = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Deleted.wav'))
reached = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'Reached.wav'))


ext_audio = {
    "main_cc": main_cc,
    "main_phelix": main_phelix,
    "story1": story1,
    "story2": story2,
    "story3": story3,
    "story4": story4,
    "post_story": post_story,
    "enter_num": enter_num,
    "retrieve_msg": retrieve_msg,
    "no_msg": no_msg,
    "post_rec": post_rec,
    "post_listen": post_listen,
    "vm_saved": vm_saved,
    "vm_deleted": vm_deleted,
    "reached": reached,
    "vm_intro": reached
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

dialtone = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'dialtone.wav'))
beep = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'keytone4.wav'))
busy_signal = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'busy_tone_loop.wav'))
disconnect = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'disconnect_tones.wav'))

test_voicemail = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'test_voicemail.wav'))

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

vm_ring = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'ringing_answer.wav'))
vm_na = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_is_not_available.wav'))

vm_not_found = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_not_a_working_number.wav'))

waymark = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'waymark_explorb.wav'))

welcome_msg = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', '6-channel44.wav'))

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

