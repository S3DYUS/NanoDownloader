import subprocess
import sys
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
PROJECT_DIR = Path(__file__).parent.resolve()
MAIN_SCRIPT = (PROJECT_DIR / "../main.py").resolve()
CONFIG_FILE = (PROJECT_DIR / "../core/config.py").resolve()
FFMPEG_BIN = (PROJECT_DIR / "../ffmpeg/bin").resolve()
ASSETS_DIR = (PROJECT_DIR / "../assets").resolve()
DEFAULT_ICON = ASSETS_DIR / "NanoDownloader.ico"

# -----------------------------
# Leer versión
# -----------------------------
def leer_version_actual():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("APP_VERSION"):
                return line.split("=")[1].strip().replace('"','').replace("'","")
    return "0.0.0"

# -----------------------------
# Actualizar versión
# -----------------------------
def escribir_version(nueva):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if line.startswith("APP_VERSION"):
                f.write(f'APP_VERSION = "{nueva}"\n')
            else:
                f.write(line)

# -----------------------------
# Build
# -----------------------------
def build_main(version, icon_path, usar_consola):

    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=NanoDownloader",
        str(MAIN_SCRIPT),
        f"--add-binary={FFMPEG_BIN / 'ffmpeg.exe'};ffmpeg/bin",
        f"--add-binary={FFMPEG_BIN / 'ffprobe.exe'};ffmpeg/bin",
        f"--add-data={ASSETS_DIR};assets",
    ]

    if not usar_consola:
        cmd.append("--windowed")

    if icon_path:
        cmd.append(f"--icon={icon_path}")

    print("\nEjecutando build:")
    print(" ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)


# -----------------------------
# Flujo
# -----------------------------
print("=== BUILD NanoDownloader ===")

version_actual = leer_version_actual()
print("Versión actual:", version_actual)

nueva_version = input("Nueva versión (enter = no cambiar): ").strip()
if nueva_version:
    escribir_version(nueva_version)
    print("Versión actualizada →", nueva_version)

icono = DEFAULT_ICON if DEFAULT_ICON.exists() else None
if not icono:
    print("⚠ No se encontró icono")

usar_consola = input("¿Mostrar consola? (s/N): ").lower() == "s"

build_main(nueva_version or version_actual, icono, usar_consola)

print("\n✅ Build completado → carpeta dist/")