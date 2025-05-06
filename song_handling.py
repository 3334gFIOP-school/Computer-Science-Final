# Sawyer Wood

import random

from save_load import load_to_playlists as load
from save_load import songs_to_save as save

# Check if a song exists in a playlist
def song_exists(playlist, song_name):
    for x in playlist:
        if x == song_name:
            return song_name  # Return the song name if it exists
    return False  # Return False if the song does not exist

# Add a song to a playlist
def add_song(playlists):

    # Prompt user for playlist name and check if it exists
    playlist = song_exists(playlists, input("Enter the name of the playlist: ")) # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if playlist == False:
        print("Playlist does not exist")
        playlists = add_song(playlists)  # Retry adding the song
        return playlists

    # Prompt user for song details
    filepath = input("Enter the file path of the song to add: ") # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name = input("Enter the name of the song: ") # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Check if the song already exists in the playlist
    for song in playlists[playlist]:
        if song[0] == name:
            print("Song already exists in the playlist")
            playlists = add_song(playlists)  # Retry adding the song
            return playlists
    
    # Add the song to the playlist
    playlists[playlist].append([name, filepath])
    return playlists

# Remove a song from a playlist
def remove_song(playlists):
    # Prompt user for playlist name and check if it exists
    playlist = song_exists(playlists, input("Enter the name of the playlist: ")) # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if playlist == False:
        print("Playlist does not exist")
        playlists = remove_song()  # Retry removing the song
        return playlists

    # Prompt user for the song name
    name = input("Enter the name of the song: ") # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Check if the song exists in the playlist and remove it
    for song in playlists[playlist]:
        if song[0] == name:
            playlists[playlist].pop(song)  # Remove the song
            return playlists
        
    print("Song does not exist in the playlist")
    playlists = remove_song(playlists)  # Retry removing the song
    return playlists

# Add a new playlist
def add_playlist(playlists):
    # Prompt user for the playlist name
    playlist_name = input("Enter the name of the playlist: ") # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Check if the playlist already exists
    if playlist_name in playlists.keys():
        print("Playlist already exists")
        playlists = add_playlist(playlists)  # Retry adding the playlist
        return playlists
    
    # Check if the playlist name is empty
    elif playlist_name == "":
        print("Playlist name cannot be empty")
        playlists = add_playlist(playlists)  # Retry adding the playlist
        return playlists
    
    # Add the new playlist
    playlists[playlist_name] = []
    return playlists

# Remove an existing playlist
def remove_playlist(playlists):
    # Prompt user for the playlist name
    playlist_name = input("Enter the name of the playlist: ") # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Check if the playlist exists and remove it
    if playlist_name in playlists.keys():
        playlists.pop(playlist_name)  # Remove the playlist
        return playlists
    else:
        print("Playlist does not exist")
        playlists = remove_playlist(playlists)  # Retry removing the playlist
        return playlists

def next_song_in_playlist(current_playlist, current_song_name):
    x = 0
    for song in current_playlist:
        x += 1
        if song[0] == current_song_name:
            return current_playlist[x][1]  # Return the next song in the playlist's file path
        
def next_shuffled_song(current_playlist, current_song_name):
    random_song = random.choice(current_playlist)

    if random_song[0] != current_song_name:
        return random_song[1]  # Return the file path of the random song
    else:
        return next_shuffled_song(current_playlist, current_song_name)
        