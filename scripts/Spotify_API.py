"""
Script to enable collection of Spotify track information using spotipy
library, which is exported as a csv file.

https://github.com/plamere/spotipy
https://developer.spotify.com/web-api/get-several-tracks/
https://developer.spotify.com/web-api/get-several-audio-features/
Requires Spotify developer access token 
(https://developer.spotify.com/web-api/authorization-guide/)
"""
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import unicodecsv



top_tracks_2017 = 'https://open.spotify.com/playlist/37i9dQZF1DX5nwnRMcdReF'
top_artists_2017 = 'https://open.spotify.com/playlist/37i9dQZF1DX9dp45EzSeyl'
top_tracks_2016 = 'https://open.spotify.com/playlist/2xKlsGov0EC2fhl6uXDgWZ'
top_tracks_2015 = 'https://open.spotify.com/playlist/6MT7PxSJmrg8O31Z5vx1iJ'
top_tracks_2014 = 'https://open.spotify.com/playlist/0KzjapF1zYpPYARZFeBnYm'
top_tracks_2013 = 'https://open.spotify.com/playlist/2kDPYiTtUtm5eZUkVYJ4f0'
top_tracks_2012 = 'https://open.spotify.com/playlist/0gbUKxGN0EdQytMEehGsoa'
top_tracks_2011_us_only = 'https://open.spotify.com/playlist/42004WRNg430hY1cShpTsR'

user = 'spotify_username'
playlist_uri = top_tracks_2015
client_id = 'client_id'
client_secret = 'client_secret'
redirect_uri = 'http://localhost:8888/callback'

# Create credentials manager and Spotify instances
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, 
                                                      client_secret=client_secret)
sp = Spotify(client_credentials_manager=client_credentials_manager)

# Get track information for chosen playlist (limited to 100 tracks per API call)
output = []
for offset in range(0,1100,100):
    playlist = sp.user_playlist_tracks(user, playlist_uri, limit=100, offset=offset)
    output += playlist['items']

# Create output dictionary with track information, including audio features
res = []
for item in output:
    row = {'artists':[]}
    for artist in item['track']['artists']:
        row['artists'].append(artist['name'])
    row['title'] = item['track']['name']
    row['explicit'] = item['track']['explicit']
    analysis = sp.audio_features([item['track']['uri']])[0]
    for key, value in analysis.items():
        row[key] = value
    res.append(row)

# Parse artist list into separate fields, clean titles
res_cleaned = []
for track in res:
    row = {}
    for key,value in track.items():
        if key == 'artists':
            row['num_artists'] = len(value)
            for i in range(0,len(value)):
                row['artist_{0}'.format(i+1)] = value[i]
        elif key == 'title':
            title = value
            if " - " in title:
                title = title[:title.find(" - ")]
            row['title'] = '"'+title+'"'
        else:
            row[key] = value
    res_cleaned.append(row)

# Prepare fields for csv export. 
# Note number of artist fields required will depend on chosen tracks/playlist
csv_fields = ['title', 'artist_1', 'artist_2', 'artist_3', 'artist_4','artist_5', 'num_artists',
              'acousticness', 'danceability', 'duration_ms', 'energy',
              'explicit', 'instrumentalness', 'key', 'liveness', 'loudness',
              'mode', 'speechiness', 'tempo', 'time_signature',
              'valence', 'type', 'analysis_url', 'track_href', 'id', 'uri']

# Export csv
with open('Spotify_Top_100.csv', 'wb') as f:
    writer = unicodecsv.DictWriter(f, csv_fields)
    writer.writeheader()
    writer.writerows(res_cleaned)