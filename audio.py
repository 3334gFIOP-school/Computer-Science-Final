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
def play_song(play_button, file_path, list_of_songs, playback_progress, current_time, total_length):  # Play or pause the song
    global is_playing, current_speed, audio_data, sample_rate, playback_thread, playback_position, volume, next_song_path
    try:
        if audio_data is None or sample_rate is None:
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

        def audio_callback(outdata, frames, time, status):
            global playback_position, is_playing, stop_bar2, next_song_path

            if not is_playing:
                raise sd.CallbackStop()

            channels = 2 if audio_data.ndim > 1 else 1
            output = np.zeros((frames, channels) if channels > 1 else (frames,), dtype=np.float32)

            for i in range(frames):
                pos = int(playback_position)
                if pos >= len(audio_data):
                    print("Song Ended")
                    stop_bar2 = True
                    is_playing = False

                    if list_of_songs:
                        next_song_path = list_of_songs.pop(0)
                        print(f"Loading next song: {next_song_path}")
                        stop_song()

                        current_time = 90
                        playback_progress["value"] = 0
                        total_length = 180
                        playback_progress["value"] = (current_time / total_length) * 100

                        play_song(play_button, next_song_path, list_of_songs, playback_progress, current_time, total_length)
                    else:
                        from main import pick_playlist
                        print("No more songs in the list. Prompting user to pick a new playlist.")
                        pick_playlist()

                    raise sd.CallbackStop()

                next_pos = min(pos + 1, len(audio_data) - 1)
                fraction = playback_position - pos

                if channels == 1:
                    sample = (1 - fraction) * audio_data[pos] + fraction * audio_data[next_pos]
                    output[i] = sample * volume
                else:
                    sample = (1 - fraction) * audio_data[pos, :] + fraction * audio_data[next_pos, :]
                    output[i, :] = sample * volume

                playback_position += current_speed

            outdata[:len(output)] = output
            if len(output) < frames:
                outdata[len(output):] = 0

        def playback_thread_func(play_button):
            global is_playing, next_song_path
            channels = 2 if audio_data.ndim > 1 else 1
            try:
                with sd.OutputStream(samplerate=sample_rate, channels=channels, dtype='float32',
                                     callback=audio_callback):

                    while is_playing:
                        sd.sleep(100)
            finally:
                play_button.config(text="▶", font=("Helvetica", 20, "bold"))
                if next_song_path:
                    path = next_song_path
                    next_song_path = None
                    stop_song()
                    play_song(play_button, path, list_of_songs, playback_progress, current_time, total_length)

        if play_button["text"] == "▶":
            is_playing = True
            try:
                playback_thread = threading.Thread(target=playback_thread_func, args=(play_button,))
            except Exception as err:
                print(f"Error creating playback thread: {err}")
                return
            playback_thread.start()
            play_button.config(text="▐▐", font=("Helvetica", 20, "bold"))
            print("Playing song")
        else:
            is_playing = False
            play_button.config(text="▶", font=("Helvetica", 20, "bold"))
            print("Paused song")

    except Exception as err:
        print(f"Error playing song: {err}")


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


# Function to seek to a specific position in the song
def seek_to_position(seconds):
    global playback_position, sample_rate
    if sample_rate:
        playback_position = seconds * sample_rate
        print(f"Seeking to {seconds}s, which is {playback_position} samples.")
