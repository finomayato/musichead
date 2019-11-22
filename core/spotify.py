import os

from spotipy import Spotify as SpotifyClient
from spotipy.oauth2 import SpotifyClientCredentials

from .common import Converter, Service, TrackMetadata

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_KEYWORDS = ['spotify']


def is_spotify_link(text: str) -> bool:
    return any(keyword in text for keyword in SPOTIFY_KEYWORDS)


class SpotifyConverter(Converter):
    def __init__(self) -> None:
        _credentials_manager = SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
        _client = SpotifyClient(client_credentials_manager=_credentials_manager)

        super().__init__()
        self.set_client(_client)

    def get_track_metadata(self, link: str) -> TrackMetadata:
        track = self._client.track(link)
        artist_name = track['artists'][0]['name']
        track_name = track['name']
        return TrackMetadata(name=track_name, artist=artist_name)

    def get_link(self, track_metadata: TrackMetadata) -> str:
        res = self._client.search(q=track_metadata.full_title, limit=1, type='track')
        track = res['tracks']['items'][0]
        return track['external_urls']['spotify']


Spotify = Service(SpotifyConverter(), is_spotify_link)
