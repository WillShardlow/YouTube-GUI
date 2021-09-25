"""GUI is alternative to command_parser"""

import tkinter as tk
from .video_player import VideoPlayer


class GUI:

    def __init__(self, video_player):
        self._player = video_player

        window = tk.Tk()

        window.geometry("480x353")
        window.title("YouTube")

        main_screen_frame = tk.Frame(window, width=450, height=253, bd=0, highlightbackground="black",
                                     highlightcolor="black", highlightthickness=1)
        main_screen_frame.pack(padx=15, pady=15)
        text_output = tk.Text(window, text="Sup, bro")
        text_output.pack()

        buttons_frame = tk.Frame(window, width=450, bg="grey")
        buttons_frame.pack()

        play_button = tk.Button(buttons_frame, text="\U000025B6", fg="black",
                                width=5, height=3, bd=0, bg="#fff")
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

        window.mainloop()

    def play_random_video(self):
        video_player.play_random_video()
