import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def is_spotify_link(text):
    return any(keyword in text for keyword in ('spotify', ))


class SpotifyConverter:
    _client = None

    def __init__(self):
        credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        self._client = spotipy.Spotify(client_credentials_manager=credentials_manager)

    def get_search_query(self, link):
        return 'Getting title for Spotify link...'

    def get_link(self, search_text):
        res = self._client.search(q=search_text, limit=1, type='track')
        track = res['tracks']['items'][0]
        return track['external_urls']['spotify']
