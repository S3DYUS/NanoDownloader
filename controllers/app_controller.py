class AppController:

    def __init__(self, worker, formats, config, bus):
        self.worker = worker
        self.formats = formats
        self.config = config
        self.bus = bus
        self.format_ids = {}

    def load_formats(self, url, modo):
        lista, ids = self.formats(url, modo)
        self.format_ids = ids
        return lista

    def start_download(self, url, modo, calidad, mp3, sub):

        opts = {
            'outtmpl': f'{self.config.get_path()}/%(title)s.%(ext)s'
        }

        if modo == "Audio":
            opts["format"] = self.format_ids.get(calidad, "bestaudio")

        if modo == "Video":
            opts["format"] = self.format_ids.get(calidad, "best")
            opts["merge_output_format"] = "mp4"

        if modo == "Subtítulos":
            opts["writesubtitles"] = True
            opts["skip_download"] = True
            opts["subtitleslangs"] = [sub]

        self.worker.download(opts, url)