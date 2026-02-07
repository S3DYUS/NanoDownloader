from yt_dlp import YoutubeDL


def limpiar(f, modo):
    if modo == "Audio":
        return f"{f.get('ext')} {int(f.get('abr',0))}kbps"
    if modo == "Video":
        return f"{f.get('ext')} {f.get('height',0)}p"
    return ""


def obtener_formatos(url, modo):
    with YoutubeDL({'listformats': True}) as ydl:
        info = ydl.extract_info(url, download=False)

    ids = {}
    lista = []

    if modo in ("Audio", "Video"):
        for f in info["formats"]:
            if modo == "Audio" and f.get("acodec") != "none":
                label = limpiar(f, modo)
                ids[label] = f["format_id"]
                lista.append(label)

            if modo == "Video" and f.get("vcodec") != "none":
                label = limpiar(f, modo)
                ids[label] = f["format_id"]
                lista.append(label)

        return sorted(set(lista), reverse=True), ids

    subs = list(info.get("subtitles", {}).keys())
    return subs or ["No disponibles"], {}