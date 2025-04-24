# Sawyer Wood

from save_load import load_to_playlists as load
from save_load import songs_to_save as save



def add_song():
    # Function to add a song to the playlist
    filepath = input("Enter the file path of the song to add: ")
    name = input("Enter the name of the song: ")


def remove_song():
    # Function to remove a song from the playlist
    pass

def add_playlist():
    # Function to add a playlist
    pass

def remove_playlist():
    # Function to remove a playlist
    pass



#Playlists format:
#playlists = {
#    playlist1name = [[song1name, song1path], [song2name, song2path], ...],
#    playlist2name = [[song1name, song1path], [song2name, song2path], ...]
#}

print(load("songs.csv"))