def is_spotify_link(text):
    return any(keyword in text for keyword in ('spotify', ))


class SpotifyConverter:
    @classmethod
    def get_title(cls, link):
        return 'Getting title for Spotify link...'

    @classmethod
    def get_link(cls, search_text):
        # TODO: search in youtube for `search_text`
        return 'Converting to Spotify link...'
