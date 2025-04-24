# Alec George

# functoins to save and load songs to csv and convert them into a readable format

import pandas as pd


#functoin to load the CSV to a dictoinary
def load(csv):
    songs = pd.read_csv(csv).to_dict()
    #make playlist list string into a list of lists
    for ind in range(len(songs['playlists'])):
        songs['playlists'][ind] = eval(songs['playlists'][ind])


    return songs


#functoin to save the dictoinary to the CSV
def save(songs, csv):

    pd.DataFrame(songs).to_csv(csv, index=False)




#functoin to re-format the dictoinary to be based on playlists
def songs_to_playlists(songs):

    playlist_dictoinary = {}
    #make a dictoinaree with keys being playlist names and values being lists of songs
    for ind, playlists in enumerate(songs['playlists'].values()):
        for playlist in playlists:
            #add the song to the playlist if the playlist is already there
            if playlist in playlist_dictoinary.keys():
                playlist_dictoinary[playlist].append(songs['song'][ind])

            #add the playlist to the dicoinary and add the song to it if the playlist wasn't already there
            else:
                playlist_dictoinary[playlist] = []
                playlist_dictoinary[playlist].append(songs['song'][ind])


    return playlist_dictoinary


#functoin to re-format the playlist dictoinary to be based on songs
def playlists_to_songs(playlists):

    songs = {
        'song': {},
        'playlists': {}
    }

    #add songs
    for ind, playlist_list in enumerate(playlists.values()):
        for i, song in enumerate(playlist_list):
            if song not in songs['song'].values():
                songs['song'][i+ind] = song
                songs['playlists'][i+ind] = []

    #add playlists
    for playlist in playlists:
        for song in playlists[playlist]:
            for ind in songs['song']:
                if songs['song'][ind] == song:
                    songs['playlists'][ind].append(playlist)

    return songs


