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

        # Define the audio callback function
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

                    # Reset progress bar and start updating for the next song
                    playback_position = 0
                    playback_progress["value"] = 0
                    playback_label.config(text="Position: 0s")
                    total_length = get_song_length(next_song_path)

                    from utils import update_progress_bar
                    is_playing = True  # Reset is_playing for the next song
                    playback_position = update_progress_bar(playback_progress, playback_label, total_length, is_playing, playback_position)

                    play_song(play_button, next_song_path, list_of_songs, playback_progress, playback_position, total_length, playback_label)
                else:
                    from main import pick_plylst
                    print("No more songs in the list. Returning to main menu.")
                    pick_plylst()
                raise sd.CallbackStop()

            next_pos = min(pos + 1, len(audio_data) - 1)
            fraction = playback_position - pos

            if channels == 1:
                sample = (1 - fraction) * audio_data[pos] + fraction * audio_data[next_pos]
                output[i] = sample * volume
            else:
                sample = (1 - fraction) * audio_data[pos, :] + fraction * audio_data[next_pos, :]
                output[i, :] = sample * volume

            playback_position += 1  # Increment playback position

        playback_position += current_speed

        outdata[:] = output

    # Define the playback thread function
    def playback_thread_func(play_button, audio_callback):
        global is_playing, next_song_path
        channels = 2 if audio_data.ndim > 1 else 1
        try:
            with sd.OutputStream(samplerate=sample_rate, channels=channels, dtype='float32', callback=audio_callback):
                while is_playing:
                    sd.sleep(100)
        finally:
            play_button.config(text="▶", font=("Helvetica", 20, "bold"))
            if next_song_path:
                path = next_song_path
                next_song_path = None
                stop_song()
                play_song(play_button, path, list_of_songs, playback_progress, current_time, total_length, playback_label)

    global is_playing
    # Start the playback thread
    if play_button["text"] == "▶":
        is_playing = True
        try:
            playback_thread = threading.Thread(target=playback_thread_func, args=(play_button, audio_callback))
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
        from utils import update_progress_bar
        update_progress_bar(playback_progress, playback_label, total_length, is_playing, playback_position)
    return current_time, playback_progress["value"], total_length

    


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