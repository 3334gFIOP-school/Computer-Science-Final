# Audio Handling - Jackson Hauley

import tkinter as tk
import pygame
from pydub import AudioSegment

def play_song(pse_ply, file_path):
    playing = True
    while playing:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)  # Parameter for file path
        pygame.mixer.music.play()
        current_text = pse_ply["text"]
        if current_text == "▶":
            # Adjust font size for "Pause" to make it visually similar to "Play"
            pse_ply.config(text="⏸", font=("Helvetica", 20, "bold"))  
            try:
                pygame.mixer.music.unpause()
                print("Playing song")
            except pygame.error as e:
                print(f"Error playing song: {e}")
        else:
            pse_ply.config(text="▶", font=("Helvetica", 20, "bold"))  
            pygame.mixer.music.pause()

def stop_song(pse_ply):
    playing = False
    pygame.mixer.music.stop() # Vincent make this work pls
    print("Stopped song")
    return playing


def set_volume(volume_slider, volume_label):
    volume = volume_slider.get() # Vincent make this work pls
    pygame.mixer.music.set_volume(volume)
    volume_label.config(text=f"Volume: {int(volume * 100)}%")  # Idk how to do this UI do it pls
    print(f"Volume set to {int(volume * 100)}%")

def change_speed(speed_slider, speed_label):
    speed = speed_slider.get() # Vincent make this work pls
    pygame.mixer.music.set_speed(speed)
    speed_label.config(text=f"Speed: {speed}") # Idk how to do this UI do it pls
    print(f"Song speed changed to {speed}")

def queue_song(file_path):
    pygame.mixer.music.queue(file_path)
    # Add UI here
    print(f"Queued song: {file_path}")

def skip_song(pse_ply,file_path):
    pygame.mixer.music.stop()
    play_song(pse_ply,file_path)
    print("Skipped song")