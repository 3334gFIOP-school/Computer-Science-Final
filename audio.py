# Audio Handling - Jackson Hauley

import tkinter as tk
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read
import threading
from save_load import *
from song_handling import *

# Global variables
is_playing = False
current_speed = 1.0
audio_data = None
sample_rate = None
playback_thread = None
playback_position = 0
volume = 1.0  # Default volume 100%
step = 1 # This fixes the broken 0.5x speed, DO NOT TOUCH

def play_song(play_button, file_path):  # Play or pause the song
    global is_playing, current_speed, audio_data, sample_rate, playback_thread, playback_position, volume
    try:
        if audio_data is None or sample_rate is None:
            sample_rate, data = read(file_path)
            if data.ndim > 1:
                print("Stereo audio detected.")  # Stereo: 2 channels
            else:
                print("Mono audio detected.")  # Mono: 1 channel

            data = data / np.max(np.abs(data))  # Normalize
            audio_data = data
            print(f"Loaded {file_path}, Sample Rate: {sample_rate}, Samples: {len(audio_data)}")

        def audio_callback(outdata, frames, time, status):
            global playback_position, is_playing

            if not is_playing:
                raise sd.CallbackStop()

            channels = 2 if audio_data.ndim > 1 else 1
            output = np.zeros((frames, channels) if channels > 1 else (frames,), dtype=np.float32)

            for i in range(frames):
                pos = int(playback_position)
                next_pos = min(pos + 1, len(audio_data) - 1)
                fraction = playback_position - pos

                if pos >= len(audio_data): # Make sure that it works
                    is_playing = False
                    break

                if channels == 1: #  Mono audio
                    sample = (1 - fraction) * audio_data[pos] + fraction * audio_data[next_pos]
                    output[i] = sample * volume
                else:
                    sample = (1 - fraction) * audio_data[pos, :] + fraction * audio_data[next_pos, :]
                    output[i, :] = sample * volume

                playback_position += current_speed

            outdata[:len(output)] = output
            if len(output) < frames:
                outdata[len(output):] = 0

        def playback_thread_func():
            global is_playing
            channels = 2 if audio_data.ndim > 1 else 1
            with sd.OutputStream(samplerate=sample_rate, channels=channels, dtype='float32', callback=audio_callback):
                while is_playing:
                    sd.sleep(100)

        if play_button["text"] == "▶️":
            is_playing = True
            # Do not reset playback_position here
            playback_thread = threading.Thread(target=playback_thread_func)
            playback_thread.start()
            play_button.config(text="⏸", font=("Helvetica", 20, "bold"))
            print("Playing song")
        else:
            is_playing = False  # Pause only (retain position)
            play_button.config(text="▶️", font=("Helvetica", 20, "bold"))
            print("Paused song")

    except Exception as err:
        print(f"Error playing song: {err}")


def stop_song(): # Stops the song
    global is_playing,current_speed, audio_data, sample_rate, playback_thread, playback_position,volume
    is_playing = False
    current_speed = 1.0
    audio_data = None
    sample_rate = None
    playback_thread = None
    playback_position = 0
    volume = 1.0  # Default volume 100%
    print("Stopped song")

def set_volume(value, label):
    try:
        global volume
        volume = round(float(value), 2)  # Convert the slider value (string) to a float
        label.config(text=f"Volume: {int(volume)}%")  # Update the label text
        print(f"Volume set to {int(volume)}%")  # Debugging output
    except Exception as e:
        print(f"Error setting volume: {e}")

def change_speed(value, label):  # Changes the speed
    global current_speed
    current_speed = round(float(value), 1)  # Convert value to float and round it
    label.config(text=f"Speed: {current_speed}x")
    print(f"Playback speed changed to {current_speed}x")

def create_replay_button(root, play_button, file_path): # Replay button
    def replay_song():
        stop_song()
        play_button.config(text="▶️", font=("Helvetica", 20, "bold"))
        play_song(play_button, file_path)
    replay_button = tk.Button(root, text="🔂", font=("Helvetica", 20, "bold"), command=replay_song)
    replay_button.pack()

def get_song_length(): # Gets the song length in seconds
    """Returns the length of the song in seconds."""
    if audio_data is not None and sample_rate is not None:
        length_in_seconds = len(audio_data) / sample_rate # Gets the song length seconds
        return length_in_seconds
    else:
        return 0  # Return 0 if audio data or sample rate is not available
    
def next_song(): # play next song
    global current_song
    temp_songlist = load_to_playlists("songs.csv")
    for x in temp_songlist:
        print(f'{x}\n{temp_songlist[x]}')
        for y in x:
            if temp_songlist[x][y] == current_song:
                next_song = temp_songlist[x][y+1]
                return next_song