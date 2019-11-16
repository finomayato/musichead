def is_spotify_link(text):
    return any(keyword in text for keyword in ('spotify', ))


class SpotifyConverter:
    def __init__(self):
        pass

    def get_search_query(self, link):
        return 'Getting title for Spotify link...'

    def get_link(self, search_text):
        # TODO: search in youtube for `search_text`
        return 'Converting to Spotify link...'
