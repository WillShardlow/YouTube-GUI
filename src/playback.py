"""A playback class"""

from .video import Video


class PlayBack:
    """A class used to represent playback."""

    def __init__(self, video=None):  # optional argument so can open PlayBack without having to play a video
        self._video = video
        self._playback_state = None

    def current_video(self):
        """Returns title of currently playing video and None if no video is playing"""

        if self._video is None:
            return None
        else:
            return self._video.title  # not .title() because video.title is not a method it is a property decorator

    def play(self):
        """Plays the current video in the player"""
        self._playback_state = "Playing"

    def pause(self):
        """Pauses the current video in the player"""
        self._playback_state = "Paused"

    def stop(self):
        """Stops the current video in the player"""
        self._video = None
        self._playback_state = None

    def change_video(self, video):
        """Changes the video in the player"""
        self._video = video


"""Video player takes video object from library, feeds video object into playback """
""""""
