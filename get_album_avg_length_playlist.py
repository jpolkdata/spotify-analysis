import os, csv, boto3, spotipy
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials

### UNCOMMENT IF RUNNING LOCALLY
# from dotenv import load_dotenv
# load_dotenv()
###

auth_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
)
spotify = spotipy.Spotify(auth_manager=auth_manager)

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

def gather_data_tmp(file_name):
    """Get Spotify data about album lengths for all artists in a given playlist.
    The end results are saved to a csv file in the /tmp/ directory
    """
    tmp_file_name = f'/tmp/{file_name}'
    with open(tmp_file_name,'w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        artists = get_artists_from_playlist(PLAYLIST)

        artists = list(artists.keys())[:3]
        for artist in artists:
            artist_name = spotify.artist(artist)['name']
            # print(f'Artist: {artist_name}')

            # get each album for the artist
            artists_albums = spotify.artist_albums(artist,album_type='album',limit=5)
            for album in artists_albums['items']:
                if album['id']:
                    # print(f"Artist: {artist_name} - Album: {album['name']}")
                    album_length = 0

                    # get each song from the album and add it to the total album length
                    songs = spotify.album_tracks(album['id'])
                    for song in songs['items']:
                        # print(f"\t{song['track_number']} - {song['name']}: {song['duration_ms']}")
                        album_length = album_length + song['duration_ms']

                # write the output to a csv that matches our desired format
                writer.writerow({'Year Released': album['release_date'][:4],
                                'Album Length': album_length,
                                'Album Name': album['name'],
                                'Artist': artist_name})

                # also write the output to our final data dictionary
                final_data_dictionary['Year Released'].append(album['release_date'][:4])
                final_data_dictionary['Album Length'].append(album_length)
                final_data_dictionary['Album Name'].append(album['name'])
                final_data_dictionary['Artist'].append(artist_name)
                
    return final_data_dictionary

def gather_data_s3(file_name):
    """Get Spotify data about album lengths for all artists in a given playlist.
    The end results are saved to an AWS S3 bucket.
    """
    gather_data_tmp(file_name)

    tmp_file_name = f'/tmp/{file_name}'
    s3_file_date = datetime.strftime(
        datetime.today(), 
        "%Y%m%d_%H%M%S")
    s3_file_name = f'{s3_file_date}_{file_name}'
    
    # write the output to the S3 bucket
    session = boto3.Session()
    s3 = session.resource('s3') 
    bucket_name = 'spotify-analysis-jpolkdata'
    response = s3.meta.client.upload_file(Filename=tmp_file_name, 
        Bucket=bucket_name, 
        Key=s3_file_name)

    return response

def lambda_handler(event, context):
    gather_data_s3('rockclassics_albums.csv')

if __name__ == "__main__":
    data = gather_data_s3('rockclassics_albums.csv')