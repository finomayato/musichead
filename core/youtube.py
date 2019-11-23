import os
from typing import Optional

from youtube_api import YouTubeDataAPI

from .common import Converter, Service, TrackMetadata
from .utils import clean_video_title

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_KEYWORDS = ['youtu.be', 'youtube']


def is_youtube_link(text: str) -> bool:
    return any(keyword in text for keyword in YOUTUBE_KEYWORDS)


# source: https://github.com/mabrownnyu/youtube-data-api/blob/master/youtube_api/youtube_api_utils.py#L79
def _strip_video_id_from_url(url: str) -> Optional[str]:
    '''Strips the video_id from YouTube URL.'''
    if '/watch?v=' in url.lower():
        return url.split('&v=')[-1].split('/watch?v=')[-1].split('?')[0].split('&')[0]
    if 'youtu.be' in url.lower():
        url_ = url[url.rindex('/') + 1:]
        if '?' in url_:
            url_ = url_[:url_.rindex('?')]
        return url_
    return None


# source: https://github.com/mabrownnyu/youtube-data-api/blob/master/youtube_api/youtube_api_utils.py#L139
def _get_url_from_video_id(video_id: str) -> str:
    '''
    Given a video id, this function returns the full URL.
    '''
    url = "https://youtube.com/watch?v={}".format(video_id)
    return url


class YouTubeConverter(Converter):
    def __init__(self) -> None:
        _client = YouTubeDataAPI(YOUTUBE_API_KEY)

        super().__init__()
        self.set_client(_client)

    def get_track_metadata(self, link: str) -> TrackMetadata:
        id_ = _strip_video_id_from_url(link)
        metadata = self._client.get_video_metadata(id_)
        return TrackMetadata(clean_video_title(metadata['video_title']))

    def get_link(self, track_metadata: TrackMetadata) -> str:
        # for simplicity only a first one is taken
        video = self._client.search(q=track_metadata.full_title, max_results=1, search_type='video')[0]
        return _get_url_from_video_id(video['video_id'])


YouTube = Service(YouTubeConverter(), is_youtube_link)
