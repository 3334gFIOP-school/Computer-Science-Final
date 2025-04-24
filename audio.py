# Audio Handling - Jackson Hauley

import tkinter as tk
import pygame

def play_song(pse_ply, file_path):
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