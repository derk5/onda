import yt_dlp

def search_youtube(query: str):
    ydl_opts = {
        "quiet": True,
        "default_search": f"ytsearch{5}",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(query, download=False)
        return [
            {
                "id": entry["id"],
                "title": entry["title"],
                "duration": entry.get("duration"),
            }
            for entry in results["entries"]
        ]

def get_stream_url(id:str):
    ydl_opts = {
        "quiet": True,
        "format": "bestaudio/best"
    }   
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            f"https://youtube.com/watch?v={id}",
            download=False
        )

    return info["url"]

def download(id: str, output = "./music"):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output}/%(id)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://youtube.com/watch?v={id}"])
    return f"{output}/{id}.mp3"


if __name__ == "__main__":
    print("Searching...")
    results = search_youtube("taste sabrina carpenter")
    
    first = results[0]
    print(f"Downloading: {first['title']}")
    path = download(first["id"])
    print(f"Saved to: {path}")