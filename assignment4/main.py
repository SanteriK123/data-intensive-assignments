import sqlite3
import pymongo

def getSql():
    return sqlite3.connect('music.db')

def getMongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client["music_nosql"]

def viewArtists():
    print("\nArtists (SQL+NOSQL):\n")
    conn = getSql()
    artists = conn.execute("SELECT * FROM artists").fetchall()
    conn.close()
    
    mongo_db = getMongo()
    
    print(f"ID | NAME | COUNTRY | BIO | WEBSITE")
    for artist in artists:
        id, name, country = artist
        
        # join the sql with nosql using id
        details = mongo_db.artist_details.find_one({"sql_id": id})
        if details:
            bio = details.get('bio')
            website = details.get('website')
        else:
            bio = "No Bio Available"
            website = "N/A"
        print(f"{id} | {name} | {country} | {bio} | {website}")

def viewArtistSeparate():
    print("\n This is the SQL part of the arists:")

    conn = getSql()
    artists = conn.execute("SELECT * FROM artists").fetchall()
    conn.close()
    
    for artist in artists:
        id, name, country = artist
        print(f'ID: {id} | Name: {name} | Country: {country}')

    print("\n This is the NoSQL part")

    mongo_db = getMongo()
    mongo_cursor = mongo_db.artist_details.find({})
    
    for detail in mongo_cursor:
        sql_id = detail.get('sql_id')
        bio = detail.get('bio')
        website = detail.get('website')
        
        print(f'SQL ID: {sql_id} | Bio: {bio} | Website: {website}')

def addArtist():
    name = input("Name: ")
    country = input("Country: ")
    bio = input("Biography: ")
    website = input("Website: ")

    conn = getSql()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO artists (name, country) VALUES (?, ?)", (name, country))
    # Get id of the last sql object
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    mongo_db = getMongo()
    mongo_db.artist_details.insert_one({
        "sql_id": new_id,
        "bio": bio,
        "website": website
    })
    
    print("Artist was added.")

def updateArtist():
    viewArtists()
    target_id = int(input("Enter ID of Artist to update: "))
 
    new_name = input("New Name: ")
    new_bio = input("New Bio: ")
    
    conn = getSql()
    conn.execute("UPDATE artists SET name = ? WHERE id = ?", (new_name, target_id))
    conn.commit()
    conn.close()

    mongo_db = getMongo()
    mongo_db.artist_details.update_one(
        {"sql_id": target_id}, 
        {"$set": {"bio": new_bio}}
    )
    print("Artist updated.")

def deleteArtist():
    target_id = int(input("Enter ID of Artist to delete: "))
    
    conn = getSql()
    conn.execute("DELETE FROM artists WHERE id = ?", (target_id,))
    conn.commit()
    conn.close()

    mongo_db = getMongo()
    mongo_db.artist_details.delete_one({"sql_id": target_id})
    
    print("Artist was deleted.")

def main():
    while True:
        print("1. View Artists")
        print("2. View Artists separately (SQL + NoSQL)")
        print("3. Add Artist")
        print("4. Update Artist")
        print("5. Delete Artist")
        print("6. Exit")
        
        choice = input("Select: ")
        
        if choice == '1': 
            viewArtists()
        elif choice == '2':
            viewArtistSeparate()
        elif choice == '3': 
            addArtist()
        elif choice == '4': 
            updateArtist()
        elif choice == '5': 
            deleteArtist()
        elif choice == '6': 
            break

if __name__ == "__main__":
    main()
