from dataclasses import dataclass
from typing import Any, Callable, Optional, Union

from spotipy import Spotify as SpotifyClient
from youtube_api import YouTubeDataAPI as YouTubeClient

FilterExpression = Callable[..., bool]


@dataclass
class TrackMetadata:
    _full_title: Optional[str] = None
    name: Optional[str] = None
    artist: Optional[str] = None

    @property
    def full_title(self) -> str:
        if self._full_title:
            return self._full_title
        if self.name and self.artist:
            return f'{self.artist} {self.name}'
        raise ValueError('Metdata does not posses enough information to get full name of the track')

    @full_title.setter
    def full_title(self, full_title: str) -> None:
        self._full_title = full_title


class Converter:
    _client: Union[SpotifyClient, YouTubeClient]

    def set_client(self, client: Any) -> None:
        self._client = client

    def get_track_metadata(self, link: str) -> TrackMetadata:
        raise NotImplementedError

    def get_link(self, track_metadata: TrackMetadata) -> str:
        raise NotImplementedError


@dataclass
class Service:
    converter: Converter
    is_convertible_link: FilterExpression

    @property
    def name(self) -> str:
        return self.__class__.__name__
