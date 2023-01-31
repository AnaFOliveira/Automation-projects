from pytube import YouTube

from .. import youtube_downloader
import pytest
import os

"""Further tests:
- test if the file has the pretended duration
- test if it has the right format .mp4
- if it has the title, duration, etc 
"""


def test_youtube_downloader():
    """Tests if youtube downloader works as expected"""
    link_to_download = "https://www.youtube.com/watch?v=vEQ8CXFWLZU"
    video = YouTube(link_to_download)
    youtube_downloader.downloader(link_to_download)
    path_out = os.path.join("./videos/", video.title)
    assert os.path.exists(path_out)


if __name__ == "__main__":
    pytest.main()
