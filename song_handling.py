# Sawyer Wood

from save_load import load_to_playlists as load
from save_load import songs_to_save as save

def song_exists(playlist, song_name):
    for x in playlist:
        if x == song_name:
            return song_name
    return False

def add_song(playlists):
    # Function to add a song to the playlist
    playlist = song_exists(playlists, input("Enter the name of the playlist: "))

    if playlist == False:
        print("Playlist does not exist")
        playlists = add_song(playlists)
        return playlists

    filepath = input("Enter the file path of the song to add: ")
    name = input("Enter the name of the song: ")

    for song in playlists[playlist]:
        if song[0] == name:
            print("Song already exists in the playlist")
            playlists = add_song(playlists)
            return playlists
    
    playlists[playlist].append([name, filepath])
    return playlists


def remove_song(playlists):
    # Function to add a song to the playlist
    playlist = song_exists(playlists, input("Enter the name of the playlist: "))

    if playlist == False:
        print("Playlist does not exist")
        playlists = remove_song()
        return playlists

    name = input("Enter the name of the song: ")

    for song in playlists[playlist]:
        if song[0] == name:
            playlists[playlist].pop(song)
            return playlists
        
    print("Song does not exist in the playlist")
    playlists = remove_song(playlists)
    return playlists

def add_playlist(playlists):

    playlist_name = input("Enter the name of the playlist: ")

    if playlist_name in playlists.keys():
        print("Playlist already exists")
        playlists = add_playlist(playlists)
        return playlists
    
    elif playlist_name == "":
        print("Playlist name cannot be empty")
        playlists = add_playlist(playlists)
        return playlists
    
    playlists[playlist_name] = []
    return playlists


def remove_playlist(playlists):

    playlist_name = input("Enter the name of the playlist: ")

    if playlist_name in playlists.keys():
        playlists.pop(playlist_name)
        return playlists
    else:
        print("Playlist does not exist")
        playlists = remove_playlist(playlists)
        return playlists


#Playlists format:
#playlists = {
#    playlist1name = [[song1name, song1path], [song2name, song2path], ...],
#    playlist2name = [[song1name, song1path], [song2name, song2path], ...]
#}
