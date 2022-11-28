import spotipy
import csv
# import boto3
# from datetime import datetime

import tools.playlists as playlists

spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())

final_data_dictionary = {
    "Year Released": [],
    "Album Length": [],
    "Album Name": [],
    "Artist": []
}

PLAYLIST = "spotify:playlist:37i9dQZF1DWXRqgorJj26U" # Rock Classics

def gather_data_local():
    with open("data/rockclassics_albums.csv",'w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        albums_obtained = []

        artists = playlists.get_artists_from_playlist(PLAYLIST)

        for artist in list(artists.values()):
            print(artist)
            # artists_albums = spotify.artist_albums(artist,album_type='album',limit=50)

            # TO DO: get each album for the artist

                # TO DO: get each song from that album and add it to the total album length


            # TO DO: write the output to a csv that matches our desired format
            writer.writerow({'Year Released': '',
                            'Album Length': '',
                            'Album Name': '',
                            'Artist': artist})

if __name__ == "__main__":
    data = gather_data_local()