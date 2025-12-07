import sqlite3
import pymongo

def setup():
    conn = sqlite3.connect('music.db')
    c = conn.cursor()
    
    # SQlite stuff

    # shared
    c.execute("CREATE TABLE IF NOT EXISTS artists (id INTEGER PRIMARY KEY, name TEXT, country TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS albums (id INTEGER PRIMARY KEY, title TEXT, year INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, title TEXT, duration INTEGER)")
    
    # Unique
    c.execute("CREATE TABLE IF NOT EXISTS merchandise (id INTEGER PRIMARY KEY, item_name TEXT, price REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS instruments (id INTEGER PRIMARY KEY, type TEXT, stock_count INTEGER)")

    c.execute("DELETE FROM artists") 
    c.execute("INSERT INTO artists (id, name, country) VALUES (1, 'Metallica', 'America')")
    c.execute("INSERT INTO artists (id, name, country) VALUES (2, 'Black Sabbath', 'UK')")
    
    conn.commit()
    conn.close()

    print("SQlite databased created")

    # Mongodb stuff
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["music_nosql"]

    # Shared artist table NOSQL (same id's as sql)
    db.artist_details.drop()
    db.artist_details.insert_many([
        {"sql_id": 1, "bio": "Legendary metal band", "website": "https://www.metallica.com/"},
        {"sql_id": 2, "bio": "Original metal band", "website": "https://www.blacksabbath.com/"}
    ])

    # Unique table playlists
    db.playlists.drop()
    db.playlists.insert_one({"name": "songs", "songs": ["Welcome to the jungle, Some song"]})
    
    # Unique table genres
    db.genres.drop()
    db.genres.insert_one({"name": "Metal", "history": "Created by Black Sabbath in 1969", "subgenres": ["Heavy Metal", "Thrash Metal"]})

    print("NoSQL database created")

if __name__ == "__main__":
    setup()
