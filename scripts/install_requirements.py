import subprocess
import sys

REQUIREMENTS = [
    "customtkinter>=5.2.0",
    "yt-dlp>=2026.01.06",
    "requests>=2.31.0",
    "packaging>=23.1",
    "pillow>=10.0.0",
    "pyinstaller>=5.15.0",
    "typing-extensions>=4.7.1"
]

def install(package):
    """Instala un paquete usando pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"[✔] {package} instalado correctamente.")
    except subprocess.CalledProcessError:
        print(f"[✖] Error instalando {package}")

def main():
    print("Instalando dependencias necesarias para NanoDownloader...\n")
    for pkg in REQUIREMENTS:
        install(pkg)
    
    print("\n¡Instalación completada!")
    print("Ahora puedes ejecutar tu aplicación o el script build.py sin problemas.")

if __name__ == "__main__":
    main()