"""Initial test of api authentication and basic Spotify search functionality"""

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
auth_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
)
spotify = spotipy.Spotify(auth_manager=auth_manager)

def get_artist_uri(name):
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    artist_uri = items[0]['uri']
    return artist_uri

def top_tracks(uri):
    results = spotify.artist_top_tracks(uri)
    for track in results['tracks'][:5]:
        print('track    : ' + track['name'])
        print('audio    : ' + track['preview_url'])
        print('cover art: ' + track['album']['images'][0]['url'])
        print()

def get_related_artists(uri):
    artists = spotify.artist_related_artists(uri)
    for artist in artists['artists'][:3]:
        print('artist       :' + artist['name'])
        print('popularity   :' + str(artist['popularity']))
        print('followers    :' + str(artist['followers'].get('total')))
        print()

if __name__ == "__main__":
    uri = get_artist_uri("Coheed and Cambria")
    top_tracks(uri)
    get_related_artists(uri)
