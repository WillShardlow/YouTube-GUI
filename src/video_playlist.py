"""A video playlist class."""

from .video import Video


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_name: str):
        self._name = playlist_name
        self._videos = []                  # list of video objects in the playlist

    @property
    def name(self) -> str:
        """Returns the name of a playlist."""
        return self._name

    def change_name(self, new_name):
        """Changes the name of a playlist"""
        self._name = new_name

    def add_video(self, video):
        """Adds a video to a playlist"""
        self._videos.append(video)

    def remove_video(self, video):
        """Removes a video from a playlist"""
        self._videos.remove(video)

    def clear(self):
        """Clears a playlist"""
        self._videos = []

    def get_all_videos(self):
        """Returns a list of all videos in a playlist"""
        return self._videos
