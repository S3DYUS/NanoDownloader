import customtkinter as ctk

from core.logger import get_logger
from core.events import EventBus
from services.config_service import ConfigService
from services.format_service import obtener_formatos
from services.ffmpeg_service import get_ffmpeg_path
from workers.download_worker import DownloadWorker
from controllers.app_controller import AppController
from ui.main_window import MainWindow


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

logger = get_logger()
bus = EventBus()
config = ConfigService()

worker = DownloadWorker(get_ffmpeg_path(), bus, logger)
controller = AppController(worker, obtener_formatos, config, bus)

app = MainWindow(controller, bus, config)
app.mainloop()