from yt_dlp import YoutubeDL


def limpiar_audio(f):
    abr = f.get("abr")
    ext = f.get("ext", "audio")
    if not abr:
        abr = 0
    return f"{ext} - {int(abr)} kbps"


def limpiar_video(f):
    ext = f.get("ext", "video")
    h = f.get("height") or 0
    return f"{ext} - {h}p"


def obtener_formatos(url, modo):
    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)

    ids = {}
    lista = []

    # ---------------- AUDIO ----------------

    if modo == "Audio":
        for f in info["formats"]:
            if f.get("acodec") != "none" and f.get("vcodec") == "none":
                label = limpiar_audio(f)

                if label not in ids:
                    ids[label] = f["format_id"]
                    lista.append(label)

        return sorted(lista, reverse=True), ids

    # ---------------- VIDEO ----------------

    if modo == "Video":
        for f in info["formats"]:
            if f.get("vcodec") != "none":
                label = limpiar_video(f)

                if label not in ids:
                    ids[label] = f["format_id"]
                    lista.append(label)

        return sorted(lista, reverse=True), ids

    # ---------------- SUBTÍTULOS ----------------

    if modo == "Subtítulos":
        subs = list(info.get("subtitles", {}).keys())
        return subs if subs else ["No disponibles"], {}

    return [], {}