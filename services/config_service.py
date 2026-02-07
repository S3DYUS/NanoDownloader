import json
from pathlib import Path
import os

CONFIG_FILE = Path("config.json")


def _default_download_path():
    """
    Devuelve la ruta por defecto:
    Carpeta Videos del usuario + NanoDownloader
    """
    videos = Path.home() / "Videos"
    ruta = videos / "NanoDownloader"
    ruta.mkdir(parents=True, exist_ok=True)
    return str(ruta)


class ConfigService:

    def __init__(self):
        self.data = self._load()

    def _load(self):
        if CONFIG_FILE.exists():
            return json.loads(CONFIG_FILE.read_text())

        # ---- default config ----
        default = {
            "download_path": _default_download_path()
        }

        CONFIG_FILE.write_text(json.dumps(default, indent=2))
        return default

    def save(self):
        CONFIG_FILE.write_text(json.dumps(self.data, indent=2))

    def get_path(self):
        path = Path(self.data["download_path"])
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    def set_path(self, p):
        Path(p).mkdir(parents=True, exist_ok=True)
        self.data["download_path"] = p
        self.save()