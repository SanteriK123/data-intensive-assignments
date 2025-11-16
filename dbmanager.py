import sqlite3

def main():
    # Terrible hard-coded values
    databases = ["db1", "db2", "db3"]
    tables = ["student", "course", "professor", "classroom", "book"]

    # Pre-define some variables for use across program
    connection_obj = None
    cursor_obj = None
    db_name = ""
    while True:
        selection = printInfo()
        if selection == "1":
            if connection_obj:
                # Close previous connection before changing

                connection_obj.close()
            db_name = input("Give the name of the database to connect to: ")
            if db_name not in databases:
                print("Database does not exist.")
                continue
            connection_obj = sqlite3.connect(db_name+".sqlite")
            cursor_obj = connection_obj.cursor()
            print(f"You are now connected to {db_name}.")
        elif selection == "2":
            createDatabases(databases)
        elif selection == "3":
            if (cursor_obj == None or db_name == ""):
                print("Please connect to a database first")
            else:
                for table in tables:
                    printTable(cursor_obj, table)
        elif selection == "4":
            select_table = input(f"Which table of {db_name} do you want to update?: ")
            updateTable(select_table, cursor_obj, connection_obj)
        elif selection == "5":
            if connection_obj:
                connection_obj.close()
            break
        print()

def printInfo():
    print("Welcome to the database manager program")
    print("1) Connect to existing database")
    print("2) Recreate databases")
    print("3) List current database contents")
    print("4) Update current database contents")
    print("5) Exit program")
    return input("Give your selection: ")

def createDatabases(names):
    number = 1
    for name in names:
        db_filename = name + ".sqlite"

        temp_conn = sqlite3.connect(db_filename)
        temp_cursor = temp_conn.cursor()

        create_tables_query = readFile("./sql/schema.sql")
        insert_data_query = readFile(f"./sql/db{number}.sql")

        temp_cursor.executescript(create_tables_query)
        temp_cursor.executescript(insert_data_query)

        temp_conn.commit()
        temp_conn.close()

        number += 1
    return 

def printTable(cursor, table):
    try:
        # Get colums and print them
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()

        # Get rows of table
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        if not rows:
            print("Table is empty)")
            return

        print(f"\nContents of {table}:")
        for column in columns:
            print(f'{column[1]} | ', end="")
        print()
        for row in rows:
            print(row)
    except:
        print("Table does not exist.")
        return

def updateTable(table_name, cursor, conn):
    printTable(cursor, table_name)
    column = input("Which column to update?: ")
    new_value = input("New value: ")
    row_id = input("ID of row: ")
    try:
        cursor.execute(f"UPDATE {table_name} SET {column} = ? WHERE id = ?", (new_value, row_id))
        conn.commit()
        print("Table updated succesfully!")
    except:
        print("Update failed!!!")
    
def readFile(file_name):
    lines = ""
    with open(file_name, "r") as f:
        lines = f.read()
    return lines

if __name__ == "__main__":
    main()
