import os
import subprocess
import sys
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
PROJECT_DIR = Path(__file__).parent.resolve()
MAIN_SCRIPT = PROJECT_DIR / "../main.py"
UPDATER_SCRIPT = PROJECT_DIR / "updater.py"
CONFIG_FILE = PROJECT_DIR / "../core/config.py"
FFMPEG_BIN = PROJECT_DIR / "../ffmpeg/bin"

# -----------------------------
# Leer versión actual desde core/config.py
# -----------------------------
def leer_version_actual():
    version = "0.0.0"
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("APP_VERSION"):
                version = line.split("=")[1].strip().replace('"','').replace("'", "")
                break
    return version

# -----------------------------
# Preguntas
# -----------------------------
print("¿Qué quieres compilar?")
print("1 - Main")
print("2 - Updater")
print("3 - Ambos")
opcion = input("Ingresa el número: ").strip()
if opcion not in ("1","2","3"):
    sys.exit("Opción inválida")

# Versión
version_actual = leer_version_actual()
print(f"Versión actual detectada: {version_actual}")
nueva_version = input("Ingresa la nueva versión (ej: 1.0.0): ").strip() if opcion in ("1","3") else version_actual
if opcion in ("1","3") and not nueva_version:
    sys.exit("Versión inválida")

# Nombre del exe
nombre_app = f"NanoDownloader"

# Icono
icono_path = input("Ruta del icono (.ico) (dejar vacío para no usar icono): ").strip()
if icono_path:
    icono_path = str(Path(icono_path).resolve())
    if not Path(icono_path).exists():
        sys.exit("Icono no encontrado.")

# Consola
usar_consola = input("¿Mostrar consola al ejecutar? (s/N): ").strip().lower() == "s"

# -----------------------------
# Helper PyInstaller
# -----------------------------
def build_exe(script_path, name, add_binaries=None, icon=None, noconsole=True):
    cmd = ["pyinstaller", "--onefile", f"--name={name}", str(script_path)]
    
    # Windowed / No console
    if noconsole:
        cmd.append("--windowed")
    
    # Binaries
    if add_binaries:
        for bin_path, dest in add_binaries:
            cmd.append(f"--add-binary={bin_path};{dest}")
    
    # Icono
    if icon:
        cmd.append(f"--icon={icon}")
    
    print("Ejecutando:", " ".join(cmd))
    subprocess.run(cmd, check=True)

# -----------------------------
# Actualizar APP_VERSION en core/config.py
# -----------------------------
if opcion in ("1","3"):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if line.startswith("APP_VERSION"):
                f.write(f'APP_VERSION = "{nueva_version}"\n')
            else:
                f.write(line)
    print(f"Versión actualizada a {nueva_version} en core/config.py")

# -----------------------------
# Build Main
# -----------------------------
if opcion in ("1","3"):
    build_exe(
        MAIN_SCRIPT,
        nombre_app,
        add_binaries=[
            (str(FFMPEG_BIN / "ffmpeg.exe"), "ffmpeg/bin"),
            (str(FFMPEG_BIN / "ffprobe.exe"), "ffmpeg/bin")
        ],
        icon=icono_path if icono_path else None,
        noconsole=not usar_consola  # true si no quieres consola
    )

# -----------------------------
# Build Updater
# -----------------------------
if opcion in ("2","3"):
    build_exe(
        UPDATER_SCRIPT,
        "updater",
        icon=icono_path if icono_path else None,
        noconsole=True  # updater siempre sin consola
    )

print("Build completado. Archivos en dist/")