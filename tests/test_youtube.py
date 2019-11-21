import pytest

from core.youtube import clean_video_title


@pytest.mark.parametrize("link,cleaned_link", [
    ('(Official Video) hello [Official New Audio Video]', 'hello'),
    ('Ed Sheeran - Beautiful People (feat. Khalid) [Official Video]', 'Ed Sheeran - Beautiful People (feat. Khalid)'),
    ('Lizzo - Good As Hell (Official Video)', 'Lizzo - Good As Hell'),
    ('True Damage - GIANTS (ft. Becky G, Keke Palmer, SOYEON, DUCKWRTH, Thutmose) | League of Legends',
     'True Damage - GIANTS (ft. Becky G, Keke Palmer, SOYEON, DUCKWRTH, Thutmose)'),
])
def test_video_title_cleaning(link, cleaned_link):
    assert clean_video_title(link) == cleaned_link
