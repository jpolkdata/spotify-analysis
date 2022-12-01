import csv
# import boto3
# from datetime import datetime
from tools.auth import get_client_credentials

spotify = get_client_credentials()

final_data_dictionary = {
    "Year Released": [],
    "Album Length": [],
    "Album Name": [],
    "Artist": []
}

PLAYLIST = "spotify:playlist:37i9dQZF1DWXRqgorJj26U" # Rock Classics

def get_artists_from_playlist(playlist_uri):
    """Get a dictionary(artist uri: artist name) of all primary artists in 
    the given playlist
    """
    artists = {}
    playlist_tracks = spotify.playlist_tracks(playlist_id=playlist_uri)
    for song in playlist_tracks['items']:
        if song['track']:
            artists[song['track']['artists'][0]['uri']] = song['track']['artists'][0]['name']
    return artists

def gather_data_local():
    """Get Spotify data about artists in a given playlist and save the end
    results locally to a csv
    """
    with open("data/rockclassics_albums.csv",'w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        albums_obtained = []

        artists = get_artists_from_playlist(PLAYLIST)

        artists = list(artists.keys())[:3]
        for artist in artists:
            artist_name = spotify.artist(artist)['name']
            # get each album for the artist
            artists_albums = spotify.artist_albums(artist,album_type='album',limit=5)
            for album in artists_albums['items']:
                if album['id']:
                    print(f"Artist: {artist_name} - Album: {album['name']}")

                    # get each song from the album and add it to the total album length
                    songs = spotify.album_tracks(album['id'])
                    for song in songs['items']:
                        print(f"\t{song['track_number']} - {song['name']}: {song['duration_ms']}")

            # write the output to a csv that matches our desired format
            writer.writerow({'Year Released': '',
                            'Album Length': '',
                            'Album Name': '',
                            'Artist': artist})

if __name__ == "__main__":
    data = gather_data_local()