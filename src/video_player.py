"""A video player class."""

from .video_library import VideoLibrary
from .playback import PlayBack
from .playlist_library import PlaylistLibrary
import random
import re


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playback = PlayBack()
        self._playlist_library = PlaylistLibrary()
        self._num_videos = len(self._video_library.get_all_videos())

    def test(self):
        '''This is a function that I can edit to test different things
        but having all the various classes and methods etc. defined.'''

        print("Enter a number and I will double it")
        num = int(input())
        print(num*2)

    @staticmethod
    def tag_printer(tags):
        """Prints the tags associated with a video in square brackets, separated by a space"""

        if tags == ():
            return '[]'
        else:
            tags_string = ''
            num_tags = len(tags)

            for i in range(num_tags-1):
                tags_string = tags_string + tags[i] + ' '
            tags_string = tags_string + tags[num_tags-1]

            return f'[{tags_string}]'

    @staticmethod
    def single_printer(video):
        """Prints all video information in a nice format"""
        return(f"{video.title} ({video.video_id}) {VideoPlayer.tag_printer(video.tags)}")

    def number_of_videos(self):
        """Returns number of videos"""
        #num_videos = len(self._video_library.get_all_videos())
        #print(f"{num_videos} videos in the library")
        # above^^ is what was already given but I've changed it

        print(f"{self._num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        list_videos = self._video_library.get_all_videos()
        list_videos.sort(key=lambda x: x.title)

        flag_dict = {}
        for video in list_videos:
            if video.flagged is True:
                flag_dict[video.video_id] = f" - FLAGGED (reason: {video.flag_reason})"
            else:
                flag_dict[video.video_id] = ""

        print("Here\'s a list of all available videos:")
        for video in list_videos:
            print("  " + VideoPlayer.single_printer(video) + flag_dict[video.video_id])

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        video = self._video_library.get_video(video_id)

        if video is None:
            print("Cannot play video: Video does not exist")
        elif video.flagged is True:
            print(f"Cannot play video: Video is currently flagged (reason: {video.flag_reason})")
        else:
            if self._playback.current_video() is not None:
                print(f"Stopping video: {self._playback.current_video()}")
            self._playback._video = video
            self._playback.play()
            print(f"Playing video: {self._playback.current_video()}")

    def stop_video(self):
        """Stops the current video."""

        if self._playback.current_video() is None:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self._playback.current_video()}")
            self._playback.stop()

    def play_random_video(self):
        """Plays a random video from the video library."""

        def not_flagged(video):
            return not video.flagged

        list_videos = self._video_library.get_all_videos()
        available_videos = list(filter(not_flagged, list_videos))

        if available_videos == []:
            print("No videos available")
        else:
            random_video = random.choice(available_videos)
            self.play_video(random_video.video_id)

    def pause_video(self):
        """Pauses the current video."""

        if self._playback.current_video() is None:
            print("Cannot pause video: No video is currently playing")
        elif self._playback._playback_state == "Paused":
            print(f"Video already paused: {self._playback.current_video()}")
        else:
            print(f"Pausing video: {self._playback.current_video()}")
            self._playback.pause()

    def continue_video(self):
        """Resumes playing the current video."""

        if self._playback.current_video() is None:
            print("Cannot continue video: No video is currently playing")
        elif self._playback._playback_state == "Playing":
            print("Cannot continue video: Video is not paused")
        else:
            print(f"Continuing video: {self._playback.current_video()}")
            self._playback.play()

    def show_playing(self):
        """Displays video currently playing."""

        current_video = self._playback._video

        if current_video is None:
            print("No video is currently playing")
        elif self._playback._playback_state == "Paused":
            print(f"Currently playing: {VideoPlayer.single_printer(current_video)} - PAUSED")
        else:
            print(f"Currently playing: {VideoPlayer.single_printer(current_video)}")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.upper() in self._playlist_library._playlists:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlist_library.new_playlist(playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        playlist = self._playlist_library.get_playlist(playlist_name)
        video = self._video_library.get_video(video_id)

        if playlist is None:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif video is None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        elif video.flagged is True:
            print(
                f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flag_reason})")
        else:
            if video in playlist._videos:
                print(f"Cannot add video to {playlist_name}: Video already added")
            else:
                playlist.add_video(video)
                print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""

        playlists = self._playlist_library.get_all_playlists()

        if playlists == []:
            print("No playlists exist yet")
        else:
            playlist_names = sorted([playlist.name for playlist in playlists])
            print("Showing all playlists:")
            for name in playlist_names:
                print("  " + name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        playlist = self._playlist_library.get_playlist(playlist_name)

        if playlist is None:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:

            playlist_videos = playlist.get_all_videos()

            flag_dict = {}
            for video in playlist_videos:
                if video.flagged is True:
                    flag_dict[video.video_id] = f" - FLAGGED (reason: {video.flag_reason})"
                else:
                    flag_dict[video.video_id] = ""

            print(f"Showing playlist: {playlist_name}")
            if playlist_videos == []:
                print("  No videos here yet")
            else:
                for video in playlist_videos:
                    print("  " + VideoPlayer.single_printer(video) + flag_dict[video.video_id])

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

        playlist = self._playlist_library.get_playlist(playlist_name)
        video = self._video_library.get_video(video_id)

        if playlist is None:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        elif video is None:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
        elif video not in playlist.get_all_videos():
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
        else:
            playlist.remove_video(video)
            print(f"Removed video from {playlist_name}: {video.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        playlist = self._playlist_library.get_playlist(playlist_name)

        if playlist is None:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            playlist.clear()
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlist_library.get_playlist(playlist_name) is None:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            self._playlist_library.delete_playlist(playlist_name)
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        def not_flagged(video):
            return not video.flagged

        list_of_all_videos = self._video_library.get_all_videos()
        available_videos = list(filter(not_flagged, list_of_all_videos))
        list_of_matched_videos = []

        for video in available_videos:
            if re.search(search_term, video.title, re.IGNORECASE):
                list_of_matched_videos.append(video)

        # for video in list_of_all_videos:
        #     if video.title.lower().find(search_term.lower()) != -1:
        #         list_of_matched_videos.append(video)

        if list_of_matched_videos == []:
            print(f"No search results for {search_term}")
        else:
            list_of_matched_videos.sort(key=lambda x: x.title)
            print(f"Here are the results for {search_term}:")
            for i in range(len(list_of_matched_videos)):
                print(f"  {i+1}) {VideoPlayer.single_printer(list_of_matched_videos[i])}")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            valid_answers = [str(i+1) for i in range(len(list_of_matched_videos))]

            ans = input()

            if ans in valid_answers:
                video_to_play = list_of_matched_videos[int(ans)-1]
                self.play_video(video_to_play.video_id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        def not_flagged(video):
            return not video.flagged

        list_of_all_videos = self._video_library.get_all_videos()
        available_videos = list(filter(not_flagged, list_of_all_videos))
        list_of_matched_videos = []

        for video in available_videos:
            if video_tag in video.tags:
                list_of_matched_videos.append(video)

        if list_of_matched_videos == []:
            print(f"No search results for {video_tag}")
        else:
            list_of_matched_videos.sort(key=lambda x: x.title)
            print(f"Here are the results for {video_tag}:")
            for i in range(len(list_of_matched_videos)):
                print(f"  {i+1}) {VideoPlayer.single_printer(list_of_matched_videos[i])}")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            valid_answers = [str(i+1) for i in range(len(list_of_matched_videos))]

            ans = input()

            if ans in valid_answers:
                video_to_play = list_of_matched_videos[int(ans)-1]
                self.play_video(video_to_play.video_id)

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        video = self._video_library.get_video(video_id)

        if video is None:
            print("Cannot flag video: Video does not exist")
        elif video.flagged is True:
            print("Cannot flag video: Video is already flagged")
        else:
            if self._playback.current_video() == video.title:
                self.stop_video()
            video.flag(flag_reason)
            print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """

        video = self._video_library.get_video(video_id)

        if video is None:
            print("Cannot remove flag from video: Video does not exist")
        elif video.flagged is False:
            print("Cannot remove flag from video: Video is not flagged")
        else:
            video.unflag()
            print(f"Successfully removed flag from video: {video.title}")
