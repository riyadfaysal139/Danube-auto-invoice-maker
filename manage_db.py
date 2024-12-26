import sqlite3
import os

def update_db():
    db_path = 'Files/DB/downloaded_files.db'

    # Ensure the directory for the database file exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Add the po_release_date column to the downloaded_files table if it doesn't exist
        cursor.execute("ALTER TABLE downloaded_files ADD COLUMN po_release_date TEXT")
        conn.commit()
        print("Database updated successfully.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column 'po_release_date' already exists.")
        else:
            print(f"Error updating database: {e}")

    # Close the connection
    conn.close()

def recreate_db():
    db_path = 'Files/DB/downloaded_files.db'

    # Ensure the directory for the database file exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop the existing table if it exists
    cursor.execute("DROP TABLE IF EXISTS downloaded_files")

    # Create the table with the new schema
    cursor.execute('''CREATE TABLE downloaded_files (file_name TEXT PRIMARY KEY, po_release_date TEXT)''')
    conn.commit()

    # Close the connection
    conn.close()
    print("Database recreated successfully.")

if __name__ == "__main__":
    action = input("Enter 'update' to update the database or 'recreate' to recreate the database: ").strip().lower()
    if action == 'update':
        update_db()
    elif action == 'recreate':
        recreate_db()
    else:
        print("Invalid action. Please enter 'update' or 'recreate'.")
