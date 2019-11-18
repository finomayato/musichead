import os

from youtube_api import YouTubeDataAPI

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


def is_youtube_link(text):
    return any(keyword in text for keyword in ('youtu.be', 'youtube'))


# got from https://github.com/mabrownnyu/youtube-data-api/blob/master/youtube_api/youtube_api_utils.py#L79
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


# got from https://github.com/mabrownnyu/youtube-data-api/blob/master/youtube_api/youtube_api_utils.py#L139
def _get_url_from_video_id(video_id):
    '''
    Given a video id, this function returns the full URL.
    '''
    url = "https://youtube.com/watch?v={}".format(video_id)
    return url


class YouTubeConverter:
    service_name = 'youtube'

    _client = None

    def __init__(self):
        self._client = YouTubeDataAPI(YOUTUBE_API_KEY)

    def get_search_query(self, link):
        id_ = _strip_video_id_from_url(link)
        metadata = self._client.get_video_metadata(id_)
        return metadata['video_title']

    def get_link(self, search_text):
        rv = self._client.search(q=search_text, max_results=1, search_type='video')
        video = rv[0]  # for simplicity - getting a first one
        return _get_url_from_video_id(video['video_id'])
