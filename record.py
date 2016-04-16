# -*- coding: utf-8 -*-
import pyaudio
import wave
import time
from datetime import datetime as dt
import subprocess as sb
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 2**11

def today_str():
    return dt.now().strftime('%Y-%m-%d')

def last_idx():
    last_file = sb.check_output('ls wav/%s_*' % today_str(), shell=True).split('\n')[-2]
    last_idx = last_file.replace('wav/%s_' % today_str(), '').replace('.wav', '')
    return int(last_idx)

def print_script(text):
        print '-' * 30
        print text
        print '-' * 30


def edit_script(file_name):
    sb.call(['vim', file_name])
    new_script = open(file_name).read().rstrip()
    print u'修正後原稿: %s' % file_name
    print_script(new_script)
    return new_script

def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)          #この中で別スレッドの処理
    return(None, pyaudio.paContinue)
 
script_files = sb.check_output('ls txt/*.txt', shell=True).split('\n')[:-1]
audio = pyaudio.PyAudio()
data_idx = last_idx() + 1

for idx, script_file in enumerate(script_files, start=data_idx):
    str_idx = str(idx).zfill(4)
    voice_id = '%s_%s' % (today_str(), str_idx)
    script = open(script_file).read().rstrip()

    key = None
    while(True):
        print u'原稿: %s' % script_file
        print_script(script)
        print u'Enterキーを押すと，録音が始まります．[e]で原稿の編集ができます'
        cmd = raw_input()
        if(cmd == 'e'):
            script = edit_script(script_file)
        frames = []
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=3,
                        frames_per_buffer=CHUNK,
                        stream_callback=callback)
        print ('recording...')
        stream.start_stream()
        # wait for stream to finish

        while(stream.is_active()):
            raw_input()
            break
        # wait for stream to finish
        print ('finished recording')

        stream.stop_stream()
        stream.close()

        # check
        print(u'今の音声で登録しますか？[y/n]')
        key = raw_input()
        if(key == 'y'): break

    # script output
    SCRIPT_OUTPUT_FILENAME = 'script/%s.txt' % voice_id
    sb.check_call('mv %s %s' % (script_file, SCRIPT_OUTPUT_FILENAME), shell=True)
    # wav output
    WAVE_OUTPUT_FILENAME = '%s.wav' % voice_id
    waveFile = wave.open('%s/%s' % ('wav', WAVE_OUTPUT_FILENAME), 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
audio.terminate()
