# Alec George


# functions to save and load songs to csv and convert them into a readable format


import pandas as pd

# function to load the CSV to a dictionary
def load(csv):
    songs = pd.read_csv(csv).to_dict()
    # make playlist list string into a list of lists
    for ind in range(len(songs['playlists'])):
        songs['playlists'][ind] = eval(songs['playlists'][ind])
    return songs



# function to save the dictionary to the CSV
def save(songs, csv):
    pd.DataFrame(songs).to_csv(csv, index=False)




# function to make a list of all songs
def list_songs(csv):
    songs = load(csv)
    song_list = []
    for i in songs['name']:
        song_list.append([songs['name'][i], songs['path'][i]])
    return song_list




# function to re-format the dictionary to be based on playlists

def songs_to_playlists(songs):
    playlist_dictoinary = {}
    # make a dictionary with keys being playlist names and values being lists of songs

    for ind, playlists in enumerate(songs['playlists'].values()):
        for playlist in playlists:
            # add the song to the playlist if the playlist is already there

            if playlist in playlist_dictoinary.keys():
                playlist_dictoinary[playlist].append([songs['name'][ind], songs['path'][ind]])
            # add the playlist to the dictionary and add the song to it if the playlist wasn't already there

            else:
                playlist_dictoinary[playlist] = []
                playlist_dictoinary[playlist].append([songs['name'][ind], songs['path'][ind]])
            # when adding songs, it will add as a list: index 0 is song name, index 1 is song path

    return playlist_dictoinary





# function to re-format the playlist dictionary to be based on songs
def playlists_to_songs(playlists):
    songs = {
        'name': {},
        'path': {},
        'playlists': {}
    }
    # variable for length of songs

    length = 0
    # add songs
    for ind, playlist_list in enumerate(playlists.values()):
        for i, song in enumerate(playlist_list):
            if song[0] not in songs['name'].values():
                songs['path'][i+ind] = song[1]
                songs['name'][i+ind] = song[0]
                songs['playlists'][i+ind] = []
                length = i+ind+1

    # add playlists
    for playlist in playlists:
        for song in playlists[playlist]:
            for ind in songs['path']:
                if songs['path'][ind] == song[1]:
                    songs['playlists'][ind].append(playlist)
    # add songs that aren't in playlists

    for ind, song in enumerate(list_songs('songs.csv')):
        if song[0] not in songs['name'].values():
            songs['name'][length+ind] = song[0]
            songs['path'][length+ind] = song[1]
            songs['playlists'][length+ind] = []
    return songs





# function to load the code to the csv and format it as playlists
def load_to_playlists(csv):
    songs = load(csv)
    songs = songs_to_playlists(songs)
    return songs





# function to convert the code as songs and save it
def playlists_to_save(songs, csv):
    songs = playlists_to_songs(songs)
    save(songs, csv)




# function to get the names of a playlist
def playlist_names(playlists):
    names = []
    for i in playlists:
        names.append(i)
    return names


# function to get the songs in a playlist
def playlist_songs(playlists, name):
    songs = []
    for i in playlists[name]:
        songs.append(i)
    return songs



# function to separate a list of songs into names and paths
def sep_songs(songs):
    # get song names
    song_names = []
    for i in songs:
        song_names.append(i[0])
    # get song paths
    song_paths = []
    for i in songs:
        song_paths.append(i[1])
    return song_names, song_paths





# function to make a list of indexes of songs in a playlist compared to all songs
def song_index(csv, playlists, name):
    all_songs = list_songs(csv)
    search_songs = playlist_songs(playlists, name)
    song_indexes = []
    for search in search_songs:
        # test each song and add its index to the list
        for ind, test in enumerate(all_songs):
            if search == test:
                song_indexes.append(ind)
    return song_indexes




# function to make a list of the paths in a playlist
def playlist_song_paths(playlists, name):
    songs = playlist_songs(playlists, name)
    paths = []
    for i in songs:
        paths.append(i[1])
    return paths




# function to make a list of playlists
def list_playlists(playlists):
    playlist_list = []
    for i in playlists:
        playlist_list.append(i)
    return playlist_list
