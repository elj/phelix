#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import pyaudio
import wave
    
### recording variables ###

chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 48000
seconds = 180
filename_base = "voicemail.wav"
directory = "recordings"

current_folder = os.path.dirname(__file__)
print("recording base folder = ", current_folder)



vmStop = 0

# stream = p.open(format=sample_format,
#                 channels=channels,
#                 rate=fs,
#                 frames_per_buffer=chunk,
#                 input=True)

def start_recording_voicemail(ext):
    frames = []
    p = pyaudio.PyAudio()
    global vmStop
    print("vmStop=", vmStop)
    print("Start recording for", seconds, "seconds")
    stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
        if (vmStop == 1):
            break
    vmStop = 0
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Done recording!")
    
    ct = datetime.datetime.now()
    filename = os.path.join(current_folder, directory, ext + "-" + str(ct.year) + "-" + str(ct.month) + "-" + str(ct.day) + "-" + str(ct.hour) + "h" + str(ct.minute) + "m" + str(ct.second) + "_" + filename_base)

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def stop_recording_voicemail():
    global vmStop
    vmStop = 1
    
def reset_vmStop():
    global vmStop
    vmStop = 0

def main(args):
    print("Recording for", seconds, "seconds")
    try:
        start_recording_voicemail()
    except KeyboardInterrupt:
        print("The end")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))