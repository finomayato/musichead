import spotipy


def is_spotify_link(text):
    return any(keyword in text for keyword in ('spotify', ))


class SpotifyConverter:
    _client = None

    def __init__(self):
        self._client = spotipy.Spotify()

    def get_search_query(self, link):
        return 'Getting title for Spotify link...'

    def get_link(self, search_text):
        return 'Looking for Spotify link'
