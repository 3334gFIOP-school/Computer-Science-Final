# Audio Handling - Jackson Hauley

import tkinter as tk
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read
import threading

# Global variables for playing audio
is_playing = False
current_speed = 1.0
audio_data = None
sample_rate = None
playback_thread = None

playback_position = 0  # global playback position

def play_song(pse_ply, file_path):
    global is_playing, current_speed, audio_data, sample_rate, playback_thread, playback_position
    try:
        sample_rate, audio_data = read(file_path)
        if audio_data.ndim > 1:
            print("Stereo audio detected.")
        else:
            print("Mono audio detected.")

        audio_data = audio_data / np.max(np.abs(audio_data))  # Normalize
        print(f"Loaded {file_path}, Sample Rate: {sample_rate}, Samples: {len(audio_data)}")
        is_playing = True
        playback_position = 0  # reset position on new play
        def audio_callback(outdata, frames, time, status):
            if not is_playing:
                raise sd.CallbackStop()

            step = int(current_speed)
            playback_position = 0
            end_pos = playback_position + frames * step

            if end_pos >= len(audio_data):
                outdata[:len(audio_data[playback_position::step])] = audio_data[playback_position::step][:frames]
                outdata[len(audio_data[playback_position::step][:frames]):] = 0
            else:
                outdata[:] = audio_data[playback_position:end_pos:step][:frames]
                playback_position += frames * step

        def playback_thread_func():
            channels = 2 if audio_data.ndim > 1 else 1
            with sd.OutputStream(samplerate=sample_rate, channels=channels, callback=audio_callback):
                sd.sleep(int(len(audio_data) / sample_rate * 1000))  # Approximate wait

        playback_thread = threading.Thread(target=playback_thread_func)
        playback_thread.start()
        input('Press enter to continue')

        if pse_ply["text"] == "▶":
            pse_ply.config(text="⏸", font=("Helvetica", 20, "bold"))
            print("Playing song")
        else:
            pse_ply.config(text="▶", font=("Helvetica", 20, "bold"))
            stop_song()

    except Exception as e:
        print(f"Error playing song: {e}")
        stop_song()


def stop_song():
    global is_playing
    is_playing = False
    print("Stopped song")


def set_volume(volume_slider, volume_label):
    global audio_data
    volume = round((volume_slider.get() / 100),2)  # Normalize slider value to 0-1
    print(f"Volume slider value: {volume}")  # Debugging: Print the volume slider value
    if audio_data is not None:
        audio_data = audio_data * volume  # Adjust volume
    volume_label.config(text=f"Volume: {int(volume * 100)}%") # VINCENT =================================================
    print(f"Volume set to {int(volume * 100)}%")


def change_speed(speed_slider, speed_label):
    global current_speed
    current_speed = round(speed_slider.get(), 1)  # Get the speed value from the slider
    speed_label.config(text=f"Speed: {current_speed}x") # VINCENT =================================================
    print(f"Playback speed changed to {current_speed}x")
    
def create_replay_button(root, play_button, file_path): # VINCENT =================================================
    def replay_song():
        stop_song()
        play_song(play_button, file_path)
    replay_button = tk.Button(root, text="🔂", font=("Helvetica", 20, "bold"), command=replay_song) # VINCENT =================================================
    replay_button.pack() # btw I wrote this WITHOUT copilot like the replay song button create thing