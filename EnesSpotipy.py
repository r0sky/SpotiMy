import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import csv

#clientId and clientSecret are unique. you need to get yours from developer.spotify.com
SPOTIPY_CLIENT_ID = '###########################'
SPOTIPY_CLIENT_SECRET = '#########################'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback/'

#scope depends on what you want to do, application wants permission regard to scope
SCOPE='user-library-read user-follow-read playlist-modify-public playlist-read-private'
username='jamessahalarda'

#get token
token = util.prompt_for_user_token(username, SCOPE, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
if token:
    spotify = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

#rest is just different methods and playing on it right now

#album names of all tracks of the artist: Birdy
def getbirdysalbumnames():
    birdy_uri = '2WX2uTcsvV5OnS0inACecP'
    results = spotify.artist_albums(birdy_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])

#authanticated user's followed artists
def currentUsersFollowedArtists():
    followed_artists=spotify.current_user_followed_artists(limit=50,after=None)['artists']['items']

    for artist in followed_artists:
        print(artist['name'])

#authanticated user's followed artists who are less popular than 40 (Spotify's popularity scale is from 0 to 100)
def followedUnPopularArtists():
    followed_artists=spotify.current_user_followed_artists(limit=50,after=None)['artists']['items']

    for artist in followed_artists:
        if artist['popularity'] < 40 :
            print(artist['name'])

#print(spotify.user('anyUserId').current_user_followed_artists(limit=50,after=None)['artists']['items'])

#current user's name of all saved songs
def getNameOfAllSavedTracks():
    results = spotify.current_user_saved_tracks()
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])

    for track in tracks:
        print(track['track']['name'])

#yeah also you can get Id's of those
def getIdOfAllSavedTracks():
    results = spotify.current_user_saved_tracks(limit=10)
    tracks = results['items']

    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])

    trackId=[]
    for track in tracks:
        trackId.append(track['track']['id'])
    return trackId


#prints name of tracks which includes danceability feature more than 0.3 from given track list
def audioFeatures(idofAllTracks):
    track_features=spotify.audio_features(tracks=idofAllTracks)
    for feature in track_features:
        if feature['danceability'] > 0.300 :
            print(spotify.track(track_id=feature['id'])['name'])


#audioFeatures(getIdOfAllSavedTracks()) not working right now because of limit
#if you lower limit it works (lowering limit is not solution what i meant is:
# if you cancel while loop in getidofallsavedtracks and do this calculations for:
# only 3-5 songs it will work)


#those 2 methods are important for me right now.
#returns list of features of tracks which are not taken as parameter(user's saved tracks)
#this list is a list which includes dictionaries. each dictionary also in a list.
def getFeaturesOfAllSavedTracks():
    results = spotify.current_user_saved_tracks(limit=20)
    tracks = results['items']


    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])

    track_features=[]
    for track in tracks:
        track_features.append(spotify.audio_features(track['track']['id']))
    return track_features

#you can save all features of saved songs given by spotify in a csv file & show us your machine learning skills!
def saveCsvOfFeatures():
    track_features=getFeaturesOfAllSavedTracks()
    fields=track_features[0][0].keys()

    csv_file = "SpotiMySongs.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for data in track_features:
                writer.writerow(data[0])
    except IOError:
        print("I/O error")

saveCsvOfFeatures()
'''
@author r0sky
'''
