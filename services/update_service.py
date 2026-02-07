import requests
import tempfile
import os
import subprocess
import sys
from packaging import version
from core.config import GITHUB_OWNER, GITHUB_REPO, APP_VERSION
import shutil

def obtener_latest_release():
    """
    Obtiene la última release de GitHub y devuelve:
    - tag: la versión
    - url: URL del primer asset (instalador)
    """
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        assets = data.get("assets", [])
        if not assets:
            return None, None
        return data["tag_name"], assets[0]["browser_download_url"]
    except Exception as e:
        print(f"No se pudo obtener la última release: {e}")
        return None, None


def actualizar_app(url):
    """
    Descarga el instalador de GitHub y lo ejecuta.
    Luego cierra la app actual para permitir que el instalador haga la actualización.
    """
    ruta_instalador = os.path.join(tempfile.gettempdir(), "instalador_nano.exe")

    # Descargar el instalador
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(ruta_instalador, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    except Exception as e:
        print(f"No se pudo descargar el instalador: {e}")
        return

    # Ejecutar el instalador en un proceso separado
    try:
        subprocess.Popen([ruta_instalador], creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception as e:
        print(f"No se pudo ejecutar el instalador: {e}")
        return

    # Pequeño retraso para asegurar que el instalador se abra antes de cerrar la app
    import time
    time.sleep(0.5)

    # Cerrar la app actual para permitir que el instalador haga la actualización
    sys.exit()