#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import phone_modes as modes
import keypad
import sounddevice  ### NEED THIS to prevent silly alsa errors
import recorder

### default recording time ###
max_time = 15

filename_base = ".wav"
directory = "recordings"

current_folder = os.path.dirname(__file__)
print("VM: recording base folder = ", current_folder)


def start_recording(num):
    # Start recording
    # If user hangs up, stop recording and delete the file
    # If user presses any key, stop recording and return

    filename = os.path.join(current_folder, directory, str(num) + filename_base)

    rec = recorder.Recorder(channels=2)
    with rec.open(filename, 'wb') as recfile:
        recfile.start_recording()
        dialed = ''
        waiting = True
        start = time.time()
        print("CR: Waiting for input or timeout...")
        while waiting:
            keypad.detectKeys() # Run a single loop of checking for keys
            dialed = keypad.keysEntered
            keypad.reset_keys_entered()
            
            if modes.on_hook():
                print("Phone hung up, stopping recording")
                # Stop recording, delete voicemail, call has ended
                recfile.stop_recording()
                delete_voicemail(num)
                return

            if dialed != '':
                print("CR: dialed is", dialed)
                # If the user entered any key, exit while loop
                waiting = False
                
            if time.time() - start > max_time:
                # If max time reached on recording, exit while loop
                # TODO: add a sound to let the user know the recording is ending
                print("R: Reached max time, stopping recording")
                waiting = False
            
    # stop recording and save the file
    recfile.stop_recording()

def delete_voicemail(num):
    file_to_delete = os.path.join(current_folder, directory, num + filename_base)
    print("VM: Deleting file at", file_to_delete)
    if os.path.exists(file_to_delete):
        os.remove(file_to_delete)
        print("VM: Deleted!")
    else:
        print("VM: File at", file_to_delete, "does not exist, not deleting")
