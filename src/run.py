"""A youtube terminal simulator."""
from .video_player import VideoPlayer
from .GUI import GUI
import tkinter as tk


if __name__ == "__main__":

    video_player = VideoPlayer()
    gui = GUI(video_player)
