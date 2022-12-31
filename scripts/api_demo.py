"""Initial test of api authentication and basic Spotify search functionality"""

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
auth_manager = SpotifyClientCredentials(
    client_id=os.getenv('TF_VAR_SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('TF_VAR_SPOTIPY_CLIENT_SECRET')
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

def get_featured_playlists():
    playlists = spotify.featured_playlists(locale=None, country='US', timestamp=None, limit=20, offset=0)
    for playlist in playlists['playlists']['items']:
        print('===============')
        print(playlist['name'])
        print(playlist['description'])
        print(playlist['uri'])
        print(playlist['tracks']['total'])

def get_categories():
    categories = spotify.categories(country=None, locale=None, limit=20, offset=0)
    for category in categories['categories']['items']:
        # print(category)
        print('===============')
        print(category['name'])
        print(category['id'])

def get_category_playlists(category_name):
    categories = spotify.categories(country=None, locale=None, limit=20, offset=0)
    for category in categories['categories']['items']:
        # print(f"{category['name']}; {category['id']}")
        if category['name'] == category_name:
            category_id = category['id']
            # print(category_id)
            break
    playlists = spotify.category_playlists(category_id=category_id, country='US', limit=20, offset=0)
    print(playlists)
    for playlist in playlists['playlists']['items']:
        print('===============')
        print(playlist['name'])
        print(playlist['description'])
        print(playlist['uri'])
        print(playlist['tracks']['total'])

if __name__ == "__main__":
    # uri = get_artist_uri("Coheed and Cambria")
    # top_tracks(uri)
    # get_related_artists(uri)

    # get_featured_playlists()

    # get_categories()
    get_category_playlists('Hip-Hop')



