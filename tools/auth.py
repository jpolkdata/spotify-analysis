import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import configparser

def get_client_credentials():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    # client_credentials_manager = SpotifyClientCredentials(
    #     client_id=config.get('SPOTIFY', 'CLIENT_ID'),
    #     client_secret=config.get('SPOTIFY', 'CLIENT_SECRET')
    # )
    # spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    CLIENT_ID = config.get('SPOTIFY', 'CLIENT_ID')
    CLIENT_SECRET = config.get('SPOTIFY', 'CLIENT_SECRET')
    os.environ["SPOTIPY_CLIENT_ID"] = CLIENT_ID
    os.environ["SPOTIPY_CLIENT_SECRET"] = CLIENT_SECRET
    auth_manager = SpotifyClientCredentials()
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify
