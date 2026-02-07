import customtkinter as ctk
from tkinter import filedialog, Menu
from packaging import version

from core.config import APP_VERSION, APP_NAME
from services.update_service import obtener_latest_release, actualizar_app


class MainWindow(ctk.CTk):

    def __init__(self, controller, bus, config_service):
        super().__init__()

        self.controller = controller
        self.bus = bus
        self.config_service = config_service

        self.title(f"{APP_NAME}")
        self.geometry("650x350")
        self._centrar()

        self.formatos_ids = {}

        self._crear_menu()
        self._crear_ui()

        self.after(100, self._procesar_eventos)

    # =========================
    # Ventana
    # =========================

    def _centrar(self, w=650, h=350):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    # =========================
    # Menu
    # =========================

    def _crear_menu(self):
        menu_bar = Menu(self)
        menu_ayuda = Menu(menu_bar, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self._acerca_de)
        menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)
        self.config(menu=menu_bar)

    # =========================
    # UI
    # =========================

    def _crear_ui(self):

        # ---- URL frame ----
        frame_url = ctk.CTkFrame(self, fg_color="transparent")
        frame_url.pack(pady=10, padx=10, fill="x")

        self.label_carpeta = ctk.CTkLabel(
            frame_url,
            text=self.config_service.get_path(),
            anchor="w",
            wraplength=600
        )
        self.label_carpeta.pack(fill="x", pady=(5, 5))

        self.entry_var = ctk.StringVar()
        self.entry_var.trace_add("write", self._url_cambiada)

        self.entry = ctk.CTkEntry(frame_url, textvariable=self.entry_var)
        self.entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

        ctk.CTkButton(
            frame_url,
            text="Elegir carpeta",
            command=self._elegir_carpeta,
            width=150
        ).pack(side="left")

        # ---- modo ----
        self.modo_var = ctk.StringVar(value="Video")
        self.modo_var.trace_add("write", self._modo_cambiado)


        ctk.CTkSegmentedButton(
            self,
            values=["Video", "Audio", "Subtítulos"],
            variable=self.modo_var,
            width=400,              # ancho total del segmented button
            height=30,              # altura del botón
            font=ctk.CTkFont(size=14, weight="bold")  # tamaño y peso de fuente
        ).pack(pady=30)
        
        # ---- frame dinámico ----
        self.frame_dyn = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_dyn.pack(fill="x")

        self.sub_calidad = ctk.CTkFrame(self.frame_dyn, fg_color="transparent")
        self.calidad_var = ctk.StringVar(value="No disponibles")
        self.calidad_menu = ctk.CTkOptionMenu(
            self.sub_calidad,
            values=["No disponibles"],
            variable=self.calidad_var,
            width=150
        )
        self.calidad_menu.pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            self.sub_calidad,
            text="Actualizar calidades",
            command=self._actualizar_formatos,
            width=150
        ).pack(side="left")

        self.mp3_var = ctk.BooleanVar(value=False)
        self.mp3_check = ctk.CTkCheckBox(
            self.sub_calidad,
            text="Convertir a MP3",
            variable=self.mp3_var
        )

        # ---- subtítulos ----
        self.sub_subs = ctk.CTkFrame(self.frame_dyn, fg_color="transparent")
        self.subs_var = ctk.StringVar(value="No disponibles")

        self.subs_menu = ctk.CTkOptionMenu(
            self.sub_subs,
            values=["No disponibles"],
            variable=self.subs_var,
            width=150
        )
        self.subs_menu.pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            self.sub_subs,
            text="Actualizar subtítulos",
            command=self._actualizar_formatos,
            width=150
        ).pack(side="left")

        # ---- estado ----
        self.estado = ctk.CTkLabel(self, text="NANO DOWNLOADER", wraplength=620)
        self.estado.pack(pady=25)

        # ---- botones ----
        frame_btn = ctk.CTkFrame(self, fg_color="transparent")
        frame_btn.pack()

        self.btn_descargar = ctk.CTkButton(
            frame_btn,
            text="Descargar",
            command=self._descargar,
            width=150
        )
        self.btn_descargar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(
            frame_btn,
            text="Cancelar",
            command=self._cancelar,
            width=150,
            state="disabled"
        )
        self.btn_cancelar.pack(side="left", padx=10)

        self._modo_cambiado()

    # =========================
    # Acciones UI
    # =========================

    def _elegir_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.config_service.set_path(carpeta)
            self.label_carpeta.configure(text=carpeta)

    def _url_cambiada(self, *_):
        url = self.entry.get().strip()
        if url:
            self._actualizar_formatos()

    def _modo_cambiado(self, *_):
        self.sub_calidad.pack_forget()
        self.sub_subs.pack_forget()
        self.mp3_check.pack_forget()

        modo = self.modo_var.get()

        if modo == "Video":
            self.sub_calidad.pack(pady=5)

        elif modo == "Audio":
            self.sub_calidad.pack(pady=5)
            self.mp3_check.pack(side="left", padx=10)

        elif modo == "Subtítulos":
            self.sub_subs.pack(pady=5)

        self._actualizar_formatos()

    def _actualizar_formatos(self):
        url = self.entry.get().strip()
        if not url:
            return

        try:
            lista = self.controller.load_formats(url, self.modo_var.get())

            if self.modo_var.get() == "Subtítulos":
                self.subs_menu.configure(values=lista)
                self.subs_var.set(lista[0])
            else:
                self.calidad_menu.configure(values=lista)
                self.calidad_var.set(lista[0])

            self.estado.configure(text=f"✅ {len(lista)} opciones")

        except Exception as e:
            self.estado.configure(text=f"❌ Error formatos")

    def _descargar(self):

        url = self.entry.get().strip()
        if not url:
            self.estado.configure(text="⚠️ Ingresa URL")
            return

        self.btn_descargar.configure(state="disabled")
        self.btn_cancelar.configure(state="normal")

        self.controller.start_download(
            url=url,
            modo=self.modo_var.get(),
            calidad=self.calidad_var.get(),
            mp3=self.mp3_var.get(),
            sub=self.subs_var.get()
        )

    def _cancelar(self):
        self.controller.worker.cancel()
        self.estado.configure(text="⏹ Cancelado")
        self.btn_descargar.configure(state="normal")
        self.btn_cancelar.configure(state="disabled")

    # =========================
    # About / Update
    # =========================

    def _acerca_de(self):

        win = ctk.CTkToplevel(self)
        win.title("Acerca de")
        win.geometry("420x300")
        win.resizable(False, False)

        # --- contenido ---
        ctk.CTkLabel(
            win,
            text="NANO DOWNLOADER",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        # Crear el frame que estará detrás del label
        frame = ctk.CTkFrame(
            win,                # contenedor principal
            fg_color="#333333", # color de fondo del frame
            corner_radius=10    # bordes redondeados
        )
        frame.pack(pady=10, padx=20, fill="x")  # padding y ancho ajustable

        # Poner el label dentro del frame
        ctk.CTkLabel(
            frame,
            text="Aplicación para descargar video, audio y subtítulos de contenidos en YouTube, basada en la librería yt-dlp y ffmpeg",
            wraplength=300,     # un poco menos que el frame para que no toque bordes
            justify="center"
        ).pack(padx=10, pady=10)  # padding dentro del frame

        estado = ctk.CTkLabel(win, text="Comprobando...")
        estado.pack(pady=10)

        # -------- CENTRAR --------
        win.update_idletasks()   # ← necesario para tamaño real

        parent_x = self.winfo_x()
        parent_y = self.winfo_y()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()

        win_w = win.winfo_width()
        win_h = win.winfo_height()

        x = parent_x + (parent_w // 2) - (win_w // 2)
        y = parent_y + (parent_h // 2) - (win_h // 2)

        win.geometry(f"+{x}+{y}")

        # Modal (opcional pero recomendado)
        win.transient(self)
        win.grab_set()
        # -------------------------

        # --- update check ---
        tag, url = obtener_latest_release()

        if tag and version.parse(tag) > version.parse(APP_VERSION):
            estado.configure(text=f"Nueva versión disponible: {tag}\nSe descargará el instalador")
            ctk.CTkButton(win, text="Actualizar",
                        command=lambda: actualizar_app(url)).pack(pady=10)
        else:
            estado.configure(text=f"Actualizado a su última versión: {APP_VERSION}")
    # =========================
    # Event bus → UI
    # =========================

    def _procesar_eventos(self):

        for tipo, valor in self.bus.poll_all():

            if tipo == "estado":
                self.estado.configure(text=valor)

            elif tipo == "progress":
                self.estado.configure(text=f"⬇️ {valor}")

            elif tipo == "completed":
                self.estado.configure(text="✅ Descarga completada")
                self.btn_descargar.configure(state="normal")
                self.btn_cancelar.configure(state="disabled")

            elif tipo == "error":
                self.estado.configure(text=f"❌ {valor}")
                self.btn_descargar.configure(state="normal")
                self.btn_cancelar.configure(state="disabled")

        self.after(100, self._procesar_eventos)