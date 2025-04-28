# Audio Handling - Jackson Hauley

import tkinter as tk
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read
import threading

# Global variables
is_playing = False
current_speed = 1.0
audio_data = None
sample_rate = None
playback_thread = None
playback_position = 0
volume = 1.0  # Default volume 100%

def play_song(play_button, file_path):
    global is_playing, current_speed, audio_data, sample_rate, playback_thread, playback_position, volume

    try:
        sample_rate, data = read(file_path)
        if data.ndim > 1:
            print("Stereo audio detected.")
        else:
            print("Mono audio detected.")
        
        data = data / np.max(np.abs(data))  # Normalize
        audio_data = data
        print(f"Loaded {file_path}, Sample Rate: {sample_rate}, Samples: {len(audio_data)}")

        def audio_callback(outdata, frames, time, status):
            global playback_position, is_playing
            if not is_playing:
                raise sd.CallbackStop()

            step = int(current_speed)
            end_pos = playback_position + frames * step

            if end_pos >= len(audio_data):
                available = (len(audio_data) - playback_position) // step
                outdata[:available] = (audio_data[playback_position::step][:available]) * volume
                outdata[available:] = 0
                is_playing = False  # Stop after end
                return 
            else:
                outdata[:] = (audio_data[playback_position:end_pos:step][:frames]) * volume
                playback_position += frames * step

        def playback_thread_func():
            global is_playing
            channels = 2 if audio_data.ndim > 1 else 1
            with sd.OutputStream(samplerate=sample_rate, channels=channels, callback=audio_callback):
                while is_playing:
                    sd.sleep(100)

        if play_button["text"] == "▶":
            is_playing = True
            playback_position = 0
            playback_thread = threading.Thread(target=playback_thread_func)
            playback_thread.start()
            play_button.config(text="⏸", font=("Helvetica", 20, "bold"))
            print("Playing song")
        else:
            stop_song()
            play_button.config(text="▶", font=("Helvetica", 20, "bold"))

        if not is_playing:
            play_button.config(text="▶", font=("Helvetica", 20, "bold"))

    except Exception as e:
        print(f"Error playing song: {e}")

def stop_song():
    global is_playing
    is_playing = False
    print("Stopped song")

def set_volume(volume_slider, volume_label):
    global volume
    volume = round((volume_slider.get() / 100), 2)
    volume_label.config(text=f"Volume: {int(volume * 100)}%")
    print(f"Volume set to {int(volume * 100)}%")

def change_speed(speed_slider, speed_label):
    global current_speed
    current_speed = round(speed_slider.get(), 1)
    speed_label.config(text=f"Speed: {current_speed}x")
    print(f"Playback speed changed to {current_speed}x")

def create_replay_button(root, play_button, file_path):
    def replay_song():
        stop_song()
        play_button.config(text="▶", font=("Helvetica", 20, "bold"))
        play_song(play_button, file_path)
    replay_button = tk.Button(root, text="🔂", font=("Helvetica", 20, "bold"), command=replay_song)
    replay_button.pack()