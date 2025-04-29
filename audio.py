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
step = 1 # This fixes the broken 0.5x speed, DO NOT TOUCH

def play_song(play_button, file_path): # Play the song
    global is_playing, current_speed, audio_data, sample_rate, playback_thread, playback_position, volume

    try:
        sample_rate, data = read(file_path)
        if data.ndim > 1:
            print("Stereo audio detected.") # Stereo audio has 2 channels and both need to be modified for volume and speed
        else:
            print("Mono audio detected.") # Stereo audio has 1 channel

        data = data / np.max(np.abs(data))  # Normalize
        audio_data = data
        print(f"Loaded {file_path}, Sample Rate: {sample_rate}, Samples: {len(audio_data)}")

        def audio_callback(outdata, frames, time, status): # Callback function for audio playback
            global playback_position, is_playing

            # Stop the callback if playback is not active
            if not is_playing:
                raise sd.CallbackStop()

            # Determine the number of audio channels (mono or stereo)
            channels = 2 if audio_data.ndim > 1 else 1

            # Create an empty output buffer: shape (frames, channels) for stereo, or (frames,) for mono
            output = np.zeros((frames, channels) if channels > 1 else (frames,), dtype=np.float32)

            # Generate each output sample using interpolation
            for i in range(frames):
                pos = int(playback_position)                        # Integer part of the current position
                next_pos = min(pos + 1, len(audio_data) - 1)        # Next sample for interpolation (clamped to avoid overflow)
                fraction = playback_position - pos                  # Fractional part between samples

                # Stop playback if we've reached the end of the audio
                if pos >= len(audio_data):
                    is_playing = False
                    break

                # Linear interpolation between current and next samples
                if channels == 1:
                    # Mono: interpolate single channel
                    sample = (1 - fraction) * audio_data[pos] + fraction * audio_data[next_pos]
                    output[i] = sample * volume
                else:
                    # Stereo: interpolate both channels
                    sample = (1 - fraction) * audio_data[pos, :] + fraction * audio_data[next_pos, :]
                    output[i, :] = sample * volume

                # Advance playback position by current speed (can be fractional)
                playback_position += current_speed

            # Write the generated samples to the output buffer
            outdata[:len(output)] = output

            # Fill any remaining buffer space with silence (if playback ended early)
            if len(output) < frames:
                outdata[len(output):] = 0

        def playback_thread_func():
            global is_playing
            channels = 2 if audio_data.ndim > 1 else 1
            with sd.OutputStream(samplerate=sample_rate, channels=channels, dtype='float32', callback=audio_callback):
                while is_playing:
                    sd.sleep(100)

        if play_button["text"] == "▶":
            is_playing = True
            playback_position = 0.0  # Use float for fractional stepping
            playback_thread = threading.Thread(target=playback_thread_func) # This lets it be paused in the middle
            playback_thread.start()
            play_button.config(text="⏸", font=("Helvetica", 20, "bold"))
            print("Playing song")
        else:
            stop_song()
            play_button.config(text="▶", font=("Helvetica", 20, "bold")) # Changing the play button

        if not is_playing:
            play_button.config(text="▶", font=("Helvetica", 20, "bold")) # Changing the play button

    except Exception as err:
        print(f"Error playing song: {err}") # Error handling

def stop_song(): # Stops the song
    global is_playing
    is_playing = False
    print("Stopped song")

def set_volume(volume_slider, volume_label): # Sets the volume
    global volume
    volume = round((volume_slider.get() / 100), 2)
    volume_label.config(text=f"Volume: {int(volume * 100)}%")
    print(f"Volume set to {int(volume * 100)}%")

def change_speed(speed_slider, speed_label): # Changes the speed
    global current_speed
    current_speed = round(speed_slider.get(), 1)
    speed_label.config(text=f"Speed: {current_speed}x")
    print(f"Playback speed changed to {current_speed}x")

def create_replay_button(root, play_button, file_path): # Replay button
    def replay_song():
        stop_song()
        play_button.config(text="▶", font=("Helvetica", 20, "bold"))
        play_song(play_button, file_path)
    replay_button = tk.Button(root, text="🔂", font=("Helvetica", 20, "bold"), command=replay_song)
    replay_button.pack()

