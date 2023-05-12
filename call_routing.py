#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import phonesound
import vmrecord


extensions = {"123", "0"}

def process_call(ext):
    print("Processing call")
    if ext == "123":
        print("Extension 123")
        phonesound.play_voicemail()
        while(phonesound.pygame.mixer.get_busy()):
            time.sleep(0.1)
        vmrecord.start_recording_voicemail()
    return
    