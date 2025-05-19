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
step = 1  # This fixes the broken 0.5x speed, DO NOT TOUCH
next_song_path = None  # Path to the next song to queue after current finishes
stop_bar2 = False


def stop_bar1():
    global stop_bar2
    if stop_bar2 is True:
        return False


# Function to change speed 
def change_speed(speed_slider, speed_label):  # Changes the speed
    global current_speed
    current_speed = round(float(speed_slider), 1)  # Convert value to float and round it
    speed_label.config(text=f"Speed: {current_speed}x")
    print(f"Playback speed changed to {current_speed}x")


# Function to play the song
def play_song(play_button, file_path, list_of_songs, playback_progress, current_time, total_length, playback_label):
    global is_playing, current_speed, audio_data, sample_rate, playback_thread, playback_position, volume, next_song_path

    print("Initializing playback...")  # Debugging

    if not playback_position:
        playback_position = 0

    current_speed = 1.0
    volume = 0.5
    try:
        if audio_data is None or sample_rate is None:
            print(f"Loading audio file: {file_path}")  # Debugging
            sample_rate, data = read(file_path)
            if data.ndim > 1:
                print("Stereo audio detected.")
            else:
                print("Mono audio detected.")
            data = data / np.max(np.abs(data))  # Normalize
            audio_data = data
            print(f"Loaded {file_path}, Sample Rate: {sample_rate}, Samples: {len(audio_data)}")
            if playback_position >= len(audio_data):
                playback_position = 0
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return

    # Define the audio callback function
    def audio_callback(outdata, frames, time, status):
        global playback_position, is_playing, stop_bar2, next_song_path

        print("Audio callback triggered.")  # Debugging

        if status:
            print(f"Audio callback status: {status}")  # Debugging

        channels = 2 if audio_data.ndim > 1 else 1
        output = np.zeros((frames, channels) if channels > 1 else (frames,), dtype=np.float32)

        for i in range(frames):
            pos = int(playback_position)
            if pos >= len(audio_data):
                print("Song Ended")  # Debugging
                stop_bar2 = True
                is_playing = False
                raise sd.CallbackStop()

            output[i] = audio_data[pos] * volume
            playback_position += current_speed

        outdata[:] = output

    # Start the playback stream
    try:
        print("Starting playback stream...")  # Debugging
        stream = sd.OutputStream(callback=audio_callback, samplerate=sample_rate, channels=2)
        stream.start()
        is_playing = True
        print("Playback started.")  # Debugging
    except Exception as e:
        print(f"Error starting playback stream: {e}")  # Debugging
        return


# Function to stop the song
def stop_song():
    global is_playing, current_speed, audio_data, sample_rate, playback_thread, playback_position, volume
    is_playing = False
    current_speed = 1.0
    audio_data = None
    sample_rate = None
    playback_thread = None
    playback_position = 0
    volume = 1.0
    print("Stopped song")


# Function to set volume
def set_volume(value, label):
    try:
        global volume
        volume = round(float(value), 2)
        label.config(text=f"Volume: {int(volume * 100)}%")
        print(f"Volume set to {int(volume * 100)}%")
    except Exception as e:
        print(f"Error setting volume: {e}")


# Function to get song length
def get_song_length(file_path):
    try:
        sample_rate, data = read(file_path)
        return len(data) / sample_rate
    except Exception as e:
        print(f"Error getting song length: {e}")
        return 0
