import os

from youtube_api import YouTubeDataAPI

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


def is_youtube_link(text):
    return any(keyword in text for keyword in ('youtu.be', 'youtube'))


def _strip_video_id_from_url(url):
    '''Strips the video_id from YouTube URL.'''
    if '/watch?v=' in url.lower():
        url_ = (url.split('&v=')[-1].split('/watch?v=')[-1].split('?')[0].split('&')[0])

    elif 'youtu.be' in url.lower():
        url_ = url[url.rindex('/') + 1:]
        if '?' in url_:
            url_ = url_[:url_.rindex('?')]
    else:
        url_ = None

    return url_


class YouTubeConverter:
    def __init__(self):
        self._client = YouTubeDataAPI(YOUTUBE_API_KEY)

    def get_title(self, link):
        id_ = _strip_video_id_from_url(link)
        metadata = self._client.get_video_metadata(id_)
        return metadata['video_title']

    def get_link(self, search_text):
        # TODO: search in youtube for `search_text`
        return 'Converting to YouTube link...'
