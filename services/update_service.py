import requests, tempfile, os, shutil, subprocess, sys
from core.config import GITHUB_OWNER, GITHUB_REPO


def obtener_latest_release():
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        assets = data.get("assets", [])
        if not assets:
            return None, None
        return data["tag_name"], assets[0]["browser_download_url"]
    except:
        return None, None


def actualizar_app(url):
    ruta_actual = sys.executable
    nuevo = os.path.join(tempfile.gettempdir(), "new.exe")

    r = requests.get(url, stream=True)
    with open(nuevo, "wb") as f:
        shutil.copyfileobj(r.raw, f)

    updater = os.path.join(os.path.dirname(ruta_actual), "updater.exe")
    subprocess.Popen([updater, ruta_actual, nuevo],
                     creationflags=subprocess.CREATE_NEW_CONSOLE)
    sys.exit()