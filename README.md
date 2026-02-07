# NanoDownloader

Aplicación para descargar **video, audio y subtítulos** de YouTube, basada en [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) y con interfaz moderna en [`CustomTkinter`](https://github.com/TomSchimansky/CustomTkinter).

Permite:

- Descargar videos y audios en distintas calidades
- Convertir audio a MP3
- Descargar subtítulos

## ⚙️ Instalación de dependencias

Se recomienda usar Python 3.11+

script para instalar los requerimientos:

```
python install_requirements.py
```

### 🚀 Usando la app (Modo dev):

Ejecutar la aplicación en modo desarrollo:

```
python main.py
```

### 🛠️ Uso de build.py

El script build.py permite crear los ejecutables para la aplicación principal y el updater.

Ejecuta:

```
python build.py
```

Te pedirá seleccionar entre 3 opciones:

1 → Main → nos genera un archivo .exe de la app principal

2 → Updater → Nos genera el updater que se encargara de verificar el release de github

3 → Ambos → Hace el build de ambas cosas

Nueva versión (ej: 1.0.2) → Espera la version a la que deseas que este la app.

Ruta del icono (.ico) (opcional) → Espera un icono para la app.

Mostrar consola al ejecutar (Sí/No) → No mostrara la consola al abrir el .exe.

El script actualizará automáticamente la versión en core/config.py y generará los .exe en dist/.

### 🗂️ Ruta de descarga por defecto:

> C:\Users\<Usuario>\Videos\NanoDownloader
