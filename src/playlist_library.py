"""A playlist library class."""

from .video_playlist import Playlist


class PlaylistLibrary:
    """A class used to represent a Playlist Library."""

    def __init__(self):
        """._playlists is a dict w/ keys being the playlist name IN UPPERCASE and values
        being the playlist object - so the original name is stored in the object but can access
        using any combination of upper/lower case"""

        self._playlists = {}

    def get_playlist(self, playlist_name):
        """Returns the playlist object given the playlist name (not case sensitive)
        and None if there is no such playlist"""
        return self._playlists.get(playlist_name.upper())

    def get_all_playlists(self):
        """Returns all playlists in the library as a list"""
        return list(self._playlists.values())

    def new_playlist(self, playlist_name):
        """Creates a new blank playlist and adds it to the library"""

        new_playlist = Playlist(playlist_name)
        self._playlists[new_playlist.name.upper()] = new_playlist

    def delete_playlist(self, playlist_name):
        """Deletes playlist from the library"""
        self._playlists.pop(playlist_name.upper())

    # def add_playlist(self, playlist):
    #     self._playlists[playlist.name] = playlist
