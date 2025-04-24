# Audio Handling - Jackson Hauley

import tkinter as tk
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read
import threading

# Global variables for playback control
is_playing = False
current_speed = 1.0
audio_data = None
sample_rate = None
playback_thread = None


def play_song(pse_ply, file_path):
    global is_playing, current_speed, audio_data, sample_rate, playback_thread

    try:
        # Load the audio file
        sample_rate, audio_data = read(file_path)
        if audio_data.ndim > 1:
            print("Stereo audio detected. Configuring for stereo playback.")
        else:
            print("Mono audio detected.")

        audio_data = audio_data / np.max(np.abs(audio_data))  # Normalize audio data
        print(f"Loaded audio: {file_path}, Sample Rate: {sample_rate}, Length: {len(audio_data)} samples")

        is_playing = True

        def audio_callback(outdata, frames, time, status):
            global is_playing, current_speed, audio_data
            if not is_playing:
                raise sd.CallbackStop()

            # Calculate the number of samples to play based on the speed
            indices = np.arange(0, len(audio_data), current_speed)
            indices = indices[:frames]  # Limit to the number of frames requested
            indices = indices.astype(int)

            # Ensure indices do not exceed the length of audio_data
            if len(indices) < frames:
                outdata[:len(indices)] = audio_data[indices]
                outdata[len(indices):] = 0  # Fill the rest with silence
                raise sd.CallbackStop()  # Stop playback when data is exhausted
            else:
                outdata[:] = audio_data[indices]

        # Start playback in a separate thread
        def playback_thread_func():
            channels = 2 if audio_data.ndim > 1 else 1  # Set channels based on audio data
            with sd.OutputStream(samplerate=sample_rate, channels=channels, callback=audio_callback):
                sd.sleep(int(len(audio_data) / sample_rate * 1000))  # Wait for playback to finish

        playback_thread = threading.Thread(target=playback_thread_func)
        playback_thread.start()

        # Update the play/pause button
        current_text = pse_ply["text"]
        if current_text == "▶":
            pse_ply.config(text="⏸", font=("Helvetica", 20, "bold"))
            print("Playing song")
        else:
            pse_ply.config(text="▶", font=("Helvetica", 20, "bold"))
            stop_song()

    except Exception as e:
        print(f"Error playing song: {e}")


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
    volume_label.config(text=f"Volume: {int(volume * 100)}%")  # Update UI
    print(f"Volume set to {int(volume * 100)}%")


def change_speed(speed_slider, speed_label):
    global current_speed
    current_speed = round(speed_slider.get(), 1)  # Get the speed value from the slider
    speed_label.config(text=f"Speed: {current_speed}x")  # Update UI
    print(f"Playback speed changed to {current_speed}x")


def queue_song(file_path):
    print(f"Queued song: {file_path}")
    # This functionality is not directly supported with sounddevice.
    # You would need to implement a queue system manually.