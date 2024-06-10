#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import pyaudio
import wave
import sounddevice
import phone_modes as modes
    
### recording variables ###

chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 44100

### default recording time ###
seconds = 15

filename_base = ".wav"
directory = "recordings"

current_folder = os.path.dirname(__file__)
print("VM: recording base folder = ", current_folder)



vmRecord = 1

# stream = p.open(format=sample_format,
#                 channels=channels,
#                 rate=fs,
#                 frames_per_buffer=chunk,
#                 input=True)

def start_recording_voicemail(ext):
    frames = []
    p = pyaudio.PyAudio()
    global vmRecord
    #print("vmRecord=", vmRecord)
    print("VM: Start recording for", seconds, "seconds")
    stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)
    for i in range(0, int(fs / chunk * seconds)): # Keep recording up until the max time or interrupted
        data = stream.read(chunk)
        frames.append(data)
        if (vmRecord == 2):   # Stop recording but save the file (user is done recording)
            break
        if (vmRecord == 0):   # Stop recording and discard (user hung up)
            return
    modes.prevent_dialing()   # Change phone modes when recording times out
    vmRecord = 1
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("VM: Done recording!")
    
    ct = datetime.datetime.now()
    filename = os.path.join(current_folder, directory, str(ext) + filename_base)

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def stop_and_save_voicemail():
    global vmRecord
    vmRecord = 2

def stop_and_delete_voicemail():
    global vmRecord
    vmRecord = 0
    
def reset_vmRecord():
    global vmRecord
    vmRecord = 1

def delete_voicemail(num):
    file_to_delete = os.path.join(current_folder, directory, num + filename_base)
    print("VM: Deleting file at", file_to_delete)
    if os.path.exists(file_to_delete):
        os.remove(file_to_delete)
        print("VM: Deleted!")
    else:
        print("VM: File at", file_to_delete, "does not exist, not deleting")

def main(args):
    print("Recording for", seconds, "seconds")
    try:
        start_recording_voicemail(0)
    except KeyboardInterrupt:
        print("The end")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
