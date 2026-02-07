import threading
import os

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadCancelled


class DownloadWorker:
    """
    Worker de descarga en hilo separado.
    Maneja progreso, cancelación y eventos UI.
    """

    def __init__(self, ffmpeg_path, bus, logger):
        self.ffmpeg = ffmpeg_path
        self.bus = bus
        self.log = logger
        self.cancel_flag = False

    # -------------------------
    # Cancelación
    # -------------------------

    def cancel(self):
        self.cancel_flag = True

    # -------------------------
    # Descarga
    # -------------------------

    def download(self, opts, url):

        self.cancel_flag = False

        # ---- hook progreso ----
        def hook(d):

            if self.cancel_flag:
                raise DownloadCancelled()

            if d["status"] == "downloading":

                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloaded = d.get("downloaded_bytes", 0)

                if total > 0:
                    pct = int(downloaded * 100 / total)
                    pct_str = f"{pct}%"
                else:
                    pct_str = "?"

                filename = (
                    d.get("filename")
                    or d.get("info_dict", {}).get("title", "")
                )

                filename = os.path.basename(filename) if filename else ""

                self.bus.emit(
                    "estado",
                    f"⬇️ {pct_str} — {filename}"
                )

        # ---- opciones yt-dlp ----

        opts["progress_hooks"] = [hook]
        opts["ffmpeg_location"] = self.ffmpeg

        # ---- hilo ----

        def run():
            try:
                with YoutubeDL(opts) as ydl:
                    ydl.download([url])

                self.bus.emit("completed")

            except DownloadCancelled:
                self.bus.emit("estado", "⏹ Descarga cancelada")

            except Exception as e:
                self.log.exception("Download error")
                self.bus.emit("error", str(e))

        threading.Thread(target=run, daemon=True).start()