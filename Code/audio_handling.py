# Jackson Hauley Audio Handling
import tkinter as tk
import threading
import pygame
import tempfile
import os
from pydub import AudioSegment

class PygameAudioPlayer:
    def __init__(self, filepath):
        pygame.mixer.init()
        self.original = AudioSegment.from_wav(filepath)
        self.audio = self.original
        self.tempfile = None
        self.paused = False
        self.playing = False

    def _export_temp_audio(self):
        if self.tempfile and os.path.exists(self.tempfile.name):
            self.tempfile.close()
            os.remove(self.tempfile.name)
        self.tempfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        self.audio.export(self.tempfile.name, format="wav")
        return self.tempfile.name

    def play(self):
        def run():
            path = self._export_temp_audio()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.playing = True
        threading.Thread(target=run, daemon=True).start()

    def pause(self):
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    def resume(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    def reverse(self):
        self.audio = self.audio.reverse()
        self.play()

    def change_speed(self, speed=1.0):
        new_frame_rate = int(self.original.frame_rate * speed)
        altered = self.original._spawn(self.original.raw_data, overrides={'frame_rate': new_frame_rate})
        self.audio = altered.set_frame_rate(self.original.frame_rate)
        self.play()

# UI with tkinter
def create_ui():
    FILE_NAME = r"C:\Users\jackson.hauley\Documents\Final Project Real\Computer-Science-Final\Audio\alarm.wav"
    player = PygameAudioPlayer(FILE_NAME.replace("\\","/"))  # Must be .wav for no ffmpeg

    root = tk.Tk()
    root.title("WAV Audio Player")

    tk.Button(root, text="Play", command=player.play).pack()
    tk.Button(root, text="Pause", command=player.pause).pack()
    tk.Button(root, text="Resume", command=player.resume).pack()
    tk.Button(root, text="Reverse", command=player.reverse).pack()
    tk.Button(root, text="Speed Up", command=lambda: player.change_speed(1.5)).pack()
    tk.Button(root, text="Slow Down", command=lambda: player.change_speed(0.75)).pack()

    root.mainloop()

create_ui()