from typing import Optional
from dataclasses import dataclass


@dataclass
class TrackMetadata:
    full_title: Optional[str] = None
    name: Optional[str] = None
    artist: Optional[str] = None
    albom: Optional[str] = None

    @property
    def full_title(self):
        if self._full_title:
            return self._full_title
        elif self.name and self.artist:
            return f'{self.artist} {self.name}'
        else:
            raise ValueError('Metdata does not posses enough information to get full name of the track')
