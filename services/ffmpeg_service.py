import os
import sys

def get_ffmpeg_path():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.abspath("./ffmpeg/bin")