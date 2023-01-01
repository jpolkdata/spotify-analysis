import os, csv, re, boto3, spotipy
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials(
    client_id=os.getenv('TF_VAR_SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('TF_VAR_SPOTIPY_CLIENT_SECRET'),
    cache_handler=spotipy.MemoryCacheHandler()
)
spotify = spotipy.Spotify(auth_manager=auth_manager)

final_data_dictionary = {
    "Year Released": [],
    "Album Length": [],
    "Album Name": [],
    "Artist": []
}

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

def get_data_tmp(playlist_uri, file_name):
    """Get Spotify data about album lengths for all artists in a given playlist.
    The end results are saved to a csv file in the /tmp/ directory
    """
    with open(file_name,'w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        artists = get_artists_from_playlist(playlist_uri)

        artists = list(artists.keys())
        for artist in artists:
            artist_name = spotify.artist(artist)['name']

            # get each album for the artist
            artists_albums = spotify.artist_albums(artist,album_type='album',limit=5)
            for album in artists_albums['items']:
                if album['id']:
                    album_length = 0

                    # get each song from the album and add it to the total album length
                    songs = spotify.album_tracks(album['id'])
                    for song in songs['items']:
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
                
    # return final_data_dictionary

def move_data_to_s3(file_name):
    """Get Spotify data about album lengths for all artists in a given playlist.
    The end results are saved to an AWS S3 bucket.
    """
    s3_file_name = file_name.split('/')[-1]
    
    # write the output to the S3 bucket
    session = boto3.Session()
    s3 = session.resource('s3') 
    bucket_name = 'jpolkdata-spotify-data'
    response = s3.meta.client.upload_file(Filename=file_name, 
        Bucket=bucket_name, 
        Key=s3_file_name)

    return response

def get_playlist_name(playlist_uri):
    playlist = spotify.playlist(playlist_uri, fields=('name'), market='US', additional_types=('track', ))
    playlist_name = playlist['name']
    playlist_name = re.sub('[^a-zA-Z0-9\n\.]', '', playlist_name)
    return playlist_name

def get_file():
    playlist_uri = "spotify:playlist:37i9dQZF1DWXRqgorJj26U" # Rock Classics
    playlist_name = get_playlist_name(playlist_uri)

    # initialize the tmp directory
    tmp = '/tmp/'
    if not os.path.exists(tmp): os.makedirs(tmp)

    # generate the file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f'{tmp}{timestamp}_{playlist_name}.csv'
    get_data_tmp(playlist_uri, file_name)
    move_data_to_s3(file_name)
    
    # cleanup tmp directory
    os.remove(file_name)

def lambda_handler(event, context):
    get_file()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    get_file()