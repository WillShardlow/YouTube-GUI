"""GUI is alternative to command_parser"""

import tkinter as tk
from .video_player import VideoPlayer


class GUI:

    def __init__(self, video_player):
        # Attributes
        self._player = video_player
        self._window = tk.Tk()

        # Method execution
        self._window_properties()
        self._main_screen_frame()
        self._buttons_frame()
        self._window.mainloop()

    def _window_properties(self):
        self._window.geometry("480x353")
        self._window.title("YouTube")

    def _main_screen_frame(self):

        main_screen_frame = tk.Frame(self._window, width=450, height=253, bd=0, highlightbackground="black",
                                     highlightcolor="black", highlightthickness=1)
        main_screen_frame.pack(padx=15, pady=15)
        main_screen_frame.pack_propagate(False)
        self._text_output = tk.Text(main_screen_frame, bd=0, bg="#0D1A47", fg='white')
        self._text_output.pack(fill="both", expand=True)
        self._text_output.insert(
            tk.END, "Hello and welcome to YouTube!\nPress play to play a random video!\n")

    def _buttons_frame(self):

        buttons_frame = tk.Frame(self._window, width=450, bg="grey")
        buttons_frame.pack()

        play_button = tk.Button(buttons_frame, text="\U000025B6", fg="black",
                                width=5, height=3, bd=0, bg="#fff", command=self._play_button_command)
        pause_button = tk.Button(buttons_frame, text="\U000023F8", fg="black",
                                 width=5, height=3, bd=0, bg="#fff")
        stop_button = tk.Button(buttons_frame, text="\U000023F9", fg="black",
                                width=5, height=3, bd=0, bg="#fff")
        show_videos_button = tk.Button(buttons_frame, text="Show Videos",
                                       fg="black", width=8, height=3, bd=0, bg="#fff")
        search_button = tk.Button(buttons_frame, text="Search", fg="black",
                                  width=8, height=3, bd=0, bg="#fff")
        show_videos_button.pack(side="left")
        pause_button.pack(side="left")
        play_button.pack(side="left")
        stop_button.pack(side="left")
        search_button.pack(side="left")

    def _play_button_command(self):
        self._player.play_random_video(self._text_output)
