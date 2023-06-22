#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import phonesound
import vmrecord


extensions = {"1", "2", "3", "4", "5", "6", "7"}

def process_call(ext):
    print("Processing call")
    time.sleep(1)
    play_welcome_message(ext)
    if (ext == "6"):
        return
    else:
        vmrecord.start_recording_voicemail(ext)
    return
    
def play_welcome_message(ext):
    phonesound.play_voicemail(ext)
    while(phonesound.pygame.mixer.get_busy()):
            time.sleep(0.1)
    return 