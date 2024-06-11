#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import phone_modes as modes
import keypad
import sounddevice
import recorder

### default recording time ###
max_time = 15

filename_base = ".wav"
directory = "recordings"

current_folder = os.path.dirname(__file__)
print("VM: recording base folder = ", current_folder)

record_ok = 1

def start_recording(num):
    # Start recording
    # If user hangs up, stop recording and delete the file
    # If user presses any key, stop recording and return

    rec = recorder.Recorder(channels=2)
    with rec.open('test_record.wav', 'wb') as recfile:
        recfile.start_recording()
        dialed = ''
        waiting = True
        start = time.time()
        print("CR: Waiting for input or timeout...")
        i = 0
        while waiting:
            print("waiting", i)
            keypad.detectKeys() # Run a single loop of checking for keys?
            dialed = keypad.keysEntered
            
            if modes.on_hook():
                print("Phone hung up, stopping recording")
                # Stop recording, delete voicemail, call has ended
                recfile.stop_recording()
                # TODO: delete the file
                return

            if dialed != '':
                print("CR: dialed is", dialed)
                # If the user entered any key, exit while loop
                keypad.reset_keys_entered()
                waiting = False
                
            if time.time() - start > max_time:
                # If max time reached on recording, exit while loop
                print("R: Reached max time, stopping recording")
                waiting = False
            
                
    # stop recording and save the file
    recfile.stop_recording()
    # ~ reset_record_ok()

# ~ def interrupt_recording():
	# ~ global record_ok
	# ~ record_ok = 0

# ~ def reset_record_ok():
	# ~ global record_ok
	# ~ record_ok = 1
	
