import sqlite3
import random
import string
import time

DB_PATH = 'database.db'
NUM_RECORDS = 1_000_000
BATCH_SIZE = 100_000

def generate_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def seed_database():
    print(f"Connecting to database {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop table if exists and create a new one
    cursor.execute('DROP TABLE IF EXISTS records')
    cursor.execute('''
        CREATE TABLE records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Optionally, we can create an index on id, but primary key is already indexed.

    print(f"Starting to insert {NUM_RECORDS} records in batches of {BATCH_SIZE}...")
    start_time = time.time()

    for i in range(0, NUM_RECORDS, BATCH_SIZE):
        batch = []
        for _ in range(BATCH_SIZE):
            name = generate_random_string(15)
            email = f"{generate_random_string(8)}@example.com"
            batch.append((name, email))
        
        cursor.executemany('INSERT INTO records (name, email) VALUES (?, ?)', batch)
        conn.commit()
        print(f"Inserted {i + BATCH_SIZE} records...")

    end_time = time.time()
    conn.close()
    
    print(f"Successfully seeded {NUM_RECORDS} records in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    seed_database()
