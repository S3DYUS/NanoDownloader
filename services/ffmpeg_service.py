import os
import sys

def get_ffmpeg_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "ffmpeg", "bin", "ffmpeg.exe")
    return os.path.abspath("ffmpeg/bin/ffmpeg.exe")