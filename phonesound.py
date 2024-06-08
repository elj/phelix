#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import os
import sys
import time

# set number of desired asynchronous channels (referenced later in mixer setup)
number_of_channels = 8

# set final fadeout time
exitfade = 1000

### end custom variables ###
    
### functions and stuff go here ###

def play_dial_tone():
    dialtone.stop()
    dialtone.play(-1)
    
def stop_dial_tone():
    dialtone.fadeout(10)
    
def play_welcome_message():  #play immediately after picking up the phone, instead of a dial tone
    print("playing welcome message")
#     welcome_msg.stop()
#     time.sleep(0.3)
#     welcome_msg.play(-1)
    welcome_msg.play(-1)
    
def stop_welcome_message():
    welcome_msg.fadeout(10)

def set_key_audio(k, desired_state):
    if key_tones.get(k, 0) == 0:
        print("key not found!")
    if(desired_state):
        key_tones.get(k).play(-1)
#         if get_num_active_channels(doors[d][0]) > 0:
#             print("already playing door", d)
#         else:
#             print("playing door", d)
#             doors[d][0].play(loops=doors[d][2])
    else:
        key_tones.get(k).fadeout(10)
#         print("stopping door", d)
#         doors[d][0].fadeout(doors[d][1])

def play_ext_msg(ext):  #replace for CallingCard
    ext_vm = voicemails[ext]
    ext_vm.play()
    
def process_hangup():
    pygame.mixer.stop()
    
def play_waymark():
    waymark.play()
    
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
#c1.set_volume(0.1, 0.9)

# look for sound & music files in subfolder 'data'
#pygame.mixer.music.load(os.path.join('data', 'loophole.wav'))#load music
current_folder = os.path.dirname(__file__)
print("sounds folder = ", current_folder)

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
test_voicemail = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'test_voicemail.wav'))
# welcome_msg = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'welcome_msg.wav'))

vm_ext1 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_ext1.wav'))
vm_ext2 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_ext2.wav'))
vm_ext3 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_ext3.wav'))
vm_ext4 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_ext4.wav'))
vm_ext5 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_ext5.wav'))
vm_ext7 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'vm_ext7.wav'))

ext18007 = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'MainNumber.wav'))

waymark = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', 'waymark_explorb.wav'))

welcome_msg = pygame.mixer.Sound(os.path.join(current_folder, 'sounds', '6-channel44.wav'))

dialtone.set_volume(0.3)

voicemails = {
    "0": test_voicemail,
    "1": vm_ext1,
    "2": vm_ext2,
    "3": vm_ext3,
    "4": vm_ext4,
    "5": vm_ext5,
    "6": waymark,
    "7": vm_ext7,
    "18007": ext18007
}

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

