from pytube import YouTube
from sys import argv
import os


def downloader(link_to_download):
    """
    Downloads the video in link provided
    :param link_to_download: link of the video to download
    :return:
    """

    video = YouTube(link_to_download)
    path_out = "./videos/"

    print("Title: ", video.title)
    print("Views: ", video.views)
    print("Author: ", video.author)
    print("Date ", video.publish_date)

    if not os.path.exists(path_out):
        print("Folder doesn't exist. Creating folder")
        os.makedirs(path_out)

    res_download = video.streams.get_lowest_resolution()
    res_download.download(os.path.join(path_out, video.title))
    return 1


if __name__ == "__main__":
    link = argv[1]
    downloader(link)
