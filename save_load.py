# Alec George

# functoins to save and load songs to csv and convert them into a readable format

import pandas as pd


#functoin to save the CSV to a dictoinary
def save(csv):
    songs = pd.read_csv(csv).to_dict()
    #make playlist list strings into lists
    for ind in range(len(songs['playlists'])):
        songs['playlists'][ind] = eval(songs['playlists'][ind])


    return songs


#functoin to load the dictoinary to the CSV
def load(songs, csv):
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
    for ind, playlist_list in enumerate(playlists.values()):
        for playlist in playlist_list:
            #if the song is not already in the songs dictoinary, add the song to the songs
            if playlists not in songs['song'].values():
                songs['song'][ind] = playlist

    print(songs)


load({'song': {0:'example1', 1:'example2', 2:'example3', 3:'example4'}, 'playlists': {0:['playlist1','playlist2'],1:['playlist2','playlist3'],2:['playlist3','playlist4'],3:['playlist4','playlist1']}},'songs.csv')
songs = save('songs.csv')
print(songs)

playlists = songs_to_playlists(songs)
print(playlists)

playlists_to_songs(playlists)