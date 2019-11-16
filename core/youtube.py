
def is_youtube_link(text):
    return any(keyword in text for keyword in ('youtu.be', 'youtube'))


class YouTubeConverter:
    @classmethod
    def get_link(cls, search_text):
        # TODO: search in youtube for `search_text`
        return 'Converting to YouTube link...'
