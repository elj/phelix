#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import pyaudio
import wave
    
### recording variables ###

chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 44100
seconds = 10
filename = "latestVM.wav"



vmStop = 0

# stream = p.open(format=sample_format,
#                 channels=channels,
#                 rate=fs,
#                 frames_per_buffer=chunk,
#                 input=True)

frames = [] #empty set that will become audio data

def start_recording_voicemail():
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
    vmvmStop = 0
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Done recording!")

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