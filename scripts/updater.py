import sys
import os
import time
import shutil
import subprocess

def main():
    if len(sys.argv) < 3:
        print("Uso: updater.exe <ruta_actual_exe> <ruta_nuevo_exe>")
        sys.exit(1)

    ruta_actual = sys.argv[1]
    ruta_nuevo = sys.argv[2]

    # ---- Esperar a que la app original se cierre ----
    time.sleep(1)
    for i in range(20):
        try:
            if os.path.exists(ruta_actual):
                os.remove(ruta_actual)
            break
        except PermissionError:
            time.sleep(0.5)
        except FileNotFoundError:
            break  # ya no existe, continuar

    # ---- Reemplazar el exe ----
    try:
        shutil.move(ruta_nuevo, ruta_actual)
    except Exception as e:
        print(f"Error al reemplazar el EXE: {e}")
        sys.exit(1)

    # ---- Relanzar la app ----
    try:
        subprocess.Popen(
            [ruta_actual],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    except Exception as e:
        print(f"Error al relanzar la app: {e}")

if __name__ == "__main__":
    main()