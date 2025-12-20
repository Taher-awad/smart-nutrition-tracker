import sqlite3
import os

# Path to database.db - assumed in backend root
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database.db")

def migrate():
    print(f"Migrating database at: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("Database not found. Nothing to migrate.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "is_admin" in columns:
            print("Column 'is_admin' already exists.")
        else:
            print("Adding 'is_admin' column...")
            cursor.execute("ALTER TABLE user ADD COLUMN is_admin INTEGER DEFAULT 0")
            conn.commit()
            print("Migration successful.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
