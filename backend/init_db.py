import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(__file__), 'database')
DB_PATH = os.path.join(DB_DIR, 'campus.db')

def init_db():
    # Ensure database directory exists
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    print(f"Initializing database at: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    
    # 2. Create Posts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        caption TEXT,
        image TEXT,
        likes INTEGER DEFAULT 0,
        author TEXT DEFAULT 'Campus Student',
        author_image TEXT,
        is_announcement BOOLEAN DEFAULT 0,
        created_at TEXT NOT NULL
    )
    ''')
    
    # Ensure all columns exist in posts (migration in case db already existed without some columns)
    cursor.execute("PRAGMA table_info(posts)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'author_image' not in columns:
        print("Migrating: Adding author_image to posts table")
        cursor.execute("ALTER TABLE posts ADD COLUMN author_image TEXT")
    if 'is_announcement' not in columns:
        print("Migrating: Adding is_announcement to posts table")
        cursor.execute("ALTER TABLE posts ADD COLUMN is_announcement BOOLEAN DEFAULT 0")

    
    # 3. Create Events table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        venue TEXT NOT NULL,
        description TEXT,
        category TEXT,
        seats INTEGER,
        registered INTEGER DEFAULT 0
    )
    ''')
    
    # 4. Create Registrations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        id TEXT PRIMARY KEY,
        event TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        class_name TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    
    # 5. Create Comments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id TEXT PRIMARY KEY,
        post_id TEXT NOT NULL,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
    )
    ''')
    
    # Seed default events if events table is empty
    cursor.execute("SELECT COUNT(*) FROM events")
    if cursor.fetchone()[0] == 0:
        print("Seeding default events...")
        default_events = [
            ("AI & ML Workshop", "2026-06-10", "10:00 AM", "Seminar Hall A", 
             "Learn AI and Machine Learning from industry experts.", "Technical", 60, 0),
            ("Tech Fest 2026", "2026-06-20", "9:00 AM", "Main Ground", 
             "Annual technical festival with competitions and exhibitions.", "Fest", 300, 0),
            ("Cultural Night", "2026-06-25", "6:00 PM", "Auditorium", 
             "Annual cultural night with dance, music and drama performances.", "Cultural", 200, 0),
            ("Sports Tournament", "2026-07-01", "8:00 AM", "Sports Ground", 
             "Inter-college cricket and football championship.", "Sports", 100, 0)
        ]
        
        cursor.executemany('''
        INSERT INTO events (title, date, time, venue, description, category, seats, registered)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_events)
        
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
