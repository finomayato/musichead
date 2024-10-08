import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .track import TrackMetadata

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def is_spotify_link(text):
    return any(keyword in text for keyword in ('spotify', ))


class SpotifyConverter:
    service_name = 'spotify'

    _client = None

    def __init__(self):
        credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        self._client = spotipy.Spotify(client_credentials_manager=credentials_manager)

    def get_track_metadata(self, link):
        track = self._client.track(link)
        artist_name = track['artists'][0]['name']
        track_name = track['name']
        return TrackMetadata(name=track_name, artist=artist_name)

    def _format_search_query(self, track_metadata):
        return track_metadata.full_title

    def get_link(self, track_metadata):
        res = self._client.search(q=self._format_search_query(track_metadata), limit=1, type='track')
        track = res['tracks']['items'][0]
        return track['external_urls']['spotify']
