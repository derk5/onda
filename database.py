import sqlite3

def init_db():
    con = sqlite3.connect("music.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS songs(id INTEGER PRIMARY KEY AUTOINCREMENT,youtube_id TEXT,title TEXT,artist TEXT,duration INTEGER,play_count INTEGER DEFAULT 0,local_path TEXT,date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS play_history(id INTEGER PRIMARY KEY AUTOINCREMENT,song_id INTEGER,played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS queue(id INTEGER PRIMARY KEY AUTOINCREMENT,song_id INTEGER,position INTEGER)")
    con.commit()
    con.close()
    return


def add_song_if_not_exists(id, title, duration):
    con = sqlite3.connect("music.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM songs WHERE id = ?",(id,))
    data = cur.fetchone()
    if data == None:
        cur.execute(
            "INSERT INTO songs (id, title, duration) VALUES (?, ?, ?)",
            (id, title, duration)
        )
        con.commit()
    con.close()


