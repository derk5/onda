from fastapi import FastAPI
from starlette.responses import RedirectResponse
from streaming import search_youtube, get_stream_url
import database
import sqlite3

init_db()

app = FastAPI()
@app.get("/search")
async def search(song: str):
    results = search_youtube(song)
    return results


@app.get("/play/{id}")
async def play(id: str, title: str, duration: int):
    add_song_if_not_exists(id,title,duration)
    got_url = get_stream_url(id)
    return RedirectResponse(got_url)

@app.get("/library")
async def look_for_download():
    con = sqlite3.connect("music.db")
    cur = con.cursor()
    results = cur.execute("SELECT * FROM songs WHERE local_path IS NOT NULL").fetchall()
    con.close()
    return results
    
@app.post("/play/{id}/log")
async def log_plays(id: str):
    con = sqlite3.connect("music.db")
    cur = con.cursor()
    song = cur.execute("SELECT id FROM songs WHERE youtube_id = ?", (id,)).fetchone()
    if song is None:
        return {"error": "Song not found"}
    song_id = song[0]
    cur.execute("INSERT INTO play_history (song_id) VALUES (?)", (song_id,))
    cur.execute("UPDATE songs SET play_count = play_count + 1 WHERE youtube_id = ?", (id,))
    con.commit()
    con.close()
    return {"logged": True}