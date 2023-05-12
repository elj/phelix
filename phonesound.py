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
    dialtone.play(-1)
    
def stop_dial_tone():
    dialtone.fadeout(10)

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

def play_voicemail():
    voicemail.play()
    
def process_hangup():
    pygame.mixer.stop()
    

### end functions ###

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

pygame.init()						#initialize pygame - this is where terrible things happen
pygame.mixer.set_num_channels(number_of_channels)	# must come *after* .init

# look for sound & music files in subfolder 'data'
#pygame.mixer.music.load(os.path.join('data', 'loophole.wav'))#load music
key1s = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-1.wav'))  #load sound
key2s = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-2.wav'))  #load sound
key3s = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-3.wav'))  #load sound
key4s = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-4.wav'))  #load sound
key5s = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-5.wav'))  #load sound
key6s = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-6.wav'))  #load sound
key7s = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-7.wav'))  #load sound
key8s = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-8.wav'))  #load sound
key9s = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-9.wav'))  #load sound
keystars = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-star.wav'))  #load sound
key0s = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-0.wav'))  #load sound
keypounds = pygame.mixer.Sound(os.path.join('sounds', 'DTMF-pound.wav'))  #load sound
dialtone = pygame.mixer.Sound(os.path.join('sounds', 'dialtone.wav'))
voicemail = pygame.mixer.Sound(os.path.join('sounds', 'voicemail.wav'))

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
