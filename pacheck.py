# -*- coding: utf-8 -*-
import sys
import pyaudio
 
# check the device id
 
p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    print i, device['name']
