import os, csv, re, boto3, spotipy, io
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('TF_VAR_SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('TF_VAR_SPOTIPY_CLIENT_SECRET'),
    cache_handler=spotipy.MemoryCacheHandler()
)
spotify=spotipy.Spotify(auth_manager=auth_manager)

market='US' # limit artist/album data to those in the United States

def get_playlist_artists(playlist_uri):
    """Get a list of all primary artists from the given playlist"""
    # get the tracks for the given playlist
    results=spotify.playlist_tracks(playlist_id=playlist_uri,market=market)
    items=results['items']

    # get the primary artist from each track
    artists=[{
        'uri': track['artists'][0]['uri'],
        'name': track['artists'][0]['name']
    }
    for record in items
    for track in [record['track']]]

    # de-dupe the artists by converting to a tuple of key-value pairs, which are items in a set.
    # a set will only keep unique values, so then just convert that result back to a dict.
    no_dupes=list(set(tuple(d.items()) for d in artists))
    unique_artists=[dict(d) for d in no_dupes]

    # sort the artists by name
    sorted_artists=sorted(unique_artists, key=lambda x: x['name'])
    return sorted_artists

def get_artist_albums(artist_uri,limit):
    """Get details on each album for the given artist. This includes the year of the album release
    as well as the combined length of all tracks in that album. The results to a csv file in the /tmp/ directory
    """
    # get the albums for the given artist
    results=spotify.artist_albums(artist_uri,album_type='album',country=market,limit=limit)
    items=results['items']
    albums=[{
        'id': album['id'],
        'uri': album['uri'],
        'name': album['name'],
        'artist_name': album['artists'][0]['name'],
        'release_date': album['release_date'],
        'total_tracks': album['total_tracks']
    }
    for album in items]

    # combine the lengths of each track on the album to get the total album length
    for album in albums:
        album_tracks=spotify.album_tracks(album['id'],market=market)
        items=album_tracks['items']

        # # add a list of the individual track lengths 
        # album['tracks']=[track['duration_ms'] for track in items]
        
        # calculate the total length of the album as the sum of the individual tracks
        album['album_length']=sum(track['duration_ms'] for track in items)

    return albums

def get_playlist_name(playlist_uri):
    """Given a playlist uri, return that playlist's name"""
    playlist = spotify.playlist(playlist_uri, fields=('name'), market='US', additional_types=('track', ))
    playlist_name = playlist['name']
    playlist_name = re.sub('[^a-zA-Z0-9\n\.]', '', playlist_name)
    return playlist_name

def get_data_to_s3():
    """Given a playlist uri, get the artists from that playlist, get their albums,
    and then return the release year and total length of each of those albums. 
    The output is saved to a file in S3"""
    playlist_uri="spotify:playlist:37i9dQZF1DWXRqgorJj26U" # Rock Classics

    # from the playlist, get all albums tied to those artists
    # NOTE: I limited the amount of albums for each artist
    artists=get_playlist_artists(playlist_uri)
    all_albums=[]
    for artist in artists:
        artist_albums=get_artist_albums(artist_uri=artist['uri'],limit=20)
        all_albums.extend([album for album in artist_albums])

    # format the dataset that we need for our output files
    final_dataset=[{
        'Artist': album['artist_name'],
        'Album_Name': album['name'],
        'Year': album['release_date'][:4],
        'Length_ms': album['album_length']
    }
    for album in all_albums]
    
    # create a file-like buffer to receive S3 uploads
    file_buffer = io.StringIO()

    # write the header row
    writer = csv.DictWriter(file_buffer, fieldnames=["Artist", "Album_Name", "Year", "Length_ms"])
    writer.writeheader()

    # Write the rest of the rows
    for album in final_dataset:
        writer.writerow(album)

    # define the output file name
    playlist_name=get_playlist_name(playlist_uri)
    timestamp=datetime.now().strftime('%Y%m%d_%H%M%S')
    s3_file_name=f'{timestamp}_{playlist_name}.csv'

    # Save the buffer contents to an S3 object
    session = boto3.Session()
    s3 = session.client('s3') 
    s3.put_object(Bucket="jpolkdata-spotify-data", 
        Key=s3_file_name, 
        Body=file_buffer.getvalue().encode("utf-8")
    )

def lambda_handler(event, context):
    get_data_to_s3()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    get_data_to_s3()
