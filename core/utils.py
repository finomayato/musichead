import re


def clean_video_title(video_title: str) -> str:
    # E.g.,
    # Ed Sheeran - Beautiful People (feat. Khalid) [Official Video]
    # Lizzo - Good As Hell (Official Video)
    pollution_words_group = r'(?:official|video|audio|ft|feat)'
    search_pattern = rf'(?:\(.*{pollution_words_group}.*\)|\[.*{pollution_words_group}.*\]|\|.*)'
    compiled_pattern = re.compile(search_pattern, re.IGNORECASE)
    return re.sub(compiled_pattern, lambda x: '', video_title).strip()
