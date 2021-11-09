"""A video player class."""

from .video_library import VideoLibrary
from .playback import PlayBack
import random
import re
import tkinter as tk


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playback = PlayBack()
        self._num_videos = len(self._video_library.get_all_videos())

    def test(self, event, tag, video_id, text_output):
        '''This is a function that I can edit to test different things
        but having all the various classes and methods etc. defined.'''

        self.play_video(video_id, text_output)

    def play_on_click(self, event, tag, video_id, text_output):
        self.play_video(video_id, text_output)

    def add_highlighter(self, event, tag, text_output):
        text_output.tag_config(tag, background="white", foreground="#0D1A47")

    def remove_highlighter(self, event, tag, text_output):
        text_output.tag_config(tag, background="#0D1A47", foreground="white")

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

    def show_all_videos(self, text_output):
        """Returns all videos."""

        list_videos = self._video_library.get_all_videos()
        list_videos.sort(key=lambda x: x.title)

        flag_dict = {}
        for video in list_videos:
            if video.flagged is True:
                flag_dict[video.video_id] = f" - FLAGGED (reason: {video.flag_reason})"
            else:
                flag_dict[video.video_id] = ""

        text_output.delete(1.0, tk.END)
        if self._playback.current_video() is not None:
            self.stop_video(text_output)

        text_output.insert(tk.END, "Here\'s a list of all available videos:\n")

        for video in list_videos:
            text_output.tag_config(video.video_id)
            text_output.tag_bind(video.video_id, "<Button-1>", lambda e, video_id=video.video_id: self.play_on_click(e,
                                                                                                                     video_id, video_id, text_output))
            text_output.tag_bind(video.video_id, "<Enter>", lambda e, video_id=video.video_id: self.add_highlighter(e,
                                                                                                                    video_id, text_output))
            text_output.tag_bind(video.video_id, "<Leave>", lambda e, video_id=video.video_id: self.remove_highlighter(e,
                                                                                                                       video_id, text_output))
            text_output.insert(tk.END, "  " + VideoPlayer.single_printer(video) +
                               flag_dict[video.video_id] + "\n", video.video_id)

    def play_button(self, text_output):
        """Play button has different functionalities so this function is necessary, unlike pause button"""

        if self._playback._playback_state == "Playing":
            text_output.insert(tk.END, "Video is already playing\n")
        elif self._playback.current_video() is None:
            text_output.delete(1.0, tk.END)
            self.play_random_video(text_output)
        elif self._playback._playback_state == "Paused":
            self.continue_video(text_output)

    def play_video(self, video_id, text_output):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
            text_output: The text widget to print to
        """

        video = self._video_library.get_video(video_id)

        if video.flagged is True:
            text_output.delete(1.0, tk.END)
            text_output.insert(
                tk.END, f"Cannot play video: Video is currently flagged (reason: {video.flag_reason})\n")
        else:
            text_output.delete(1.0, tk.END)
            if self._playback.current_video() is not None:
                text_output.insert(
                    tk.END, f"Stopping video: {self._playback.current_video()}\n")
            self._playback._video = video
            self._playback.play()
            text_output.insert(
                tk.END, f"Playing video: {self._playback.current_video()}\n")

    def stop_video(self, text_output):
        """Stops the current video."""

        if self._playback.current_video() is None:
            text_output.insert(tk.END, "Cannot stop video: No video is currently playing\n")
        else:
            text_output.insert(tk.END, f"Stopping video: {self._playback.current_video()}\n")
            self._playback.stop()

    def play_random_video(self, text_output):
        """Plays a random video from the video library."""

        def not_flagged(video):
            return not video.flagged

        list_videos = self._video_library.get_all_videos()
        available_videos = list(filter(not_flagged, list_videos))

        if available_videos == []:
            text_output.insert(tk.END, "No videos available\n")
        else:
            random_video = random.choice(available_videos)
            self.play_video(random_video.video_id, text_output)

    def pause_video(self, text_output):
        """Pauses the current video."""

        if self._playback.current_video() is None:
            text_output.insert(tk.END, "Cannot pause video: No video is currently playing\n")
        elif self._playback._playback_state == "Paused":
            text_output.insert(tk.END, f"Video already paused: {self._playback.current_video()}\n")
        else:
            text_output.insert(tk.END, f"Pausing video: {self._playback.current_video()}\n")
            self._playback.pause()

    def continue_video(self, text_output):
        """Resumes playing the current video."""

        if self._playback.current_video() is None:
            text_output.insert(tk.END, "Cannot continue video: No video is currently playing\n")
        elif self._playback._playback_state == "Playing":
            text_output.insert(tk.END, "Cannot continue video: Video is not paused\n")
        else:
            text_output.insert(tk.END, f"Continuing video: {self._playback.current_video()}\n")
            self._playback.play()

    def search_button(self, text_output):

        pop_up = tk.Toplevel()
        pop_up.title("Search")
        pop_up.geometry("300x100")

        label = tk.Label(pop_up, text="What would you like to search for?")
        entry = tk.Entry(pop_up, width=25)
        label.pack(expand=True)
        entry.pack(expand=True)
        entry.focus()

        pop_up.bind('<Return>', lambda e: self.search_videos(e, pop_up, text_output, entry.get()))

    def search_videos(self, event, pop_up_window, text_output, search_term):
        """Display all the videos whose titles contain the search_term."""

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

        text_output.delete(1.0, tk.END)

        if list_of_matched_videos == []:
            text_output.insert(
                tk.END, f"No search results for {search_term}\n")
        else:
            list_of_matched_videos.sort(key=lambda x: x.title)
            text_output.insert(
                tk.END, f"Here are the results for {search_term}:\n")
            for video in list_of_matched_videos:
                text_output.tag_config(video.video_id)
                text_output.tag_bind(video.video_id, "<Button-1>", lambda e, video_id=video.video_id: self.play_on_click(e,
                                                                                                                         video_id, video_id, text_output))
                text_output.tag_bind(video.video_id, "<Enter>", lambda e, video_id=video.video_id: self.add_highlighter(e,
                                                                                                                        video_id, text_output))
                text_output.tag_bind(video.video_id, "<Leave>", lambda e, video_id=video.video_id: self.remove_highlighter(e,
                                                                                                                           video_id, text_output))
                text_output.insert(
                    tk.END, f"  {VideoPlayer.single_printer(video)}\n", video.video_id)

        pop_up_window.destroy()

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
