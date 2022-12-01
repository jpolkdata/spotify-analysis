import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import configparser

def get_client_credentials():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    client_credentials_manager = SpotifyClientCredentials(
        client_id=config.get('SPOTIFY', 'CLIENT_ID'),
        client_secret=config.get('SPOTIFY', 'CLIENT_SECRET')
    )
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return spotify