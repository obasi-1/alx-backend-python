import asyncio
import aiosqlite
import time

# --- Setup Database (Synchronous for initial setup) ---
def setup_database():
    """
    Sets up the 'users.db' database and populates it with dummy data,
    including users with various ages for testing.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    ''')
    # Insert some dummy data, ensuring some users are older than 40
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (1, 'Alice Smith', 'alice@example.com', 30)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (2, 'Bob Johnson', 'bob@example.com', 22)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (3, 'Charlie Brown', 'charlie@example.com', 45)") # Older
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (4, 'Diana Prince', 'diana@example.com', 28)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (5, 'Eve Adams', 'eve@example.com', 50)")     # Older
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (6, 'Frank White', 'frank@example.com', 38)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (7, 'Grace Green', 'grace@example.com', 60)") # Older
    conn.commit()
    conn.close()
    print("Database 'users.db' and table 'users' ensured to exist with dummy data.")

# --- Asynchronous Database Functions ---

async def async_fetch_users():
    """
    Asynchronously fetches all users from the 'users' table.
    Simulates a small delay to highlight concurrency.
    """
    print("Starting async_fetch_users...")
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            await asyncio.sleep(0.1) # Simulate I/O bound operation
            users = await cursor.fetchall()
            print("Finished async_fetch_users.")
            return users

async def async_fetch_older_users(age_threshold=40):
    """
    Asynchronously fetches users older than a specified age from the 'users' table.
    Simulates a small delay to highlight concurrency.
    """
    print(f"Starting async_fetch_older_users (age > {age_threshold})...")
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (age_threshold,)) as cursor:
            await asyncio.sleep(0.2) # Simulate I/O bound operation
            older_users = await cursor.fetchall()
            print(f"Finished async_fetch_older_users (age > {age_threshold}).")
            return older_users

async def fetch_concurrently():
    """
    Executes multiple asynchronous database queries concurrently using asyncio.gather().
    """
    print("\n--- Running concurrent fetches ---")
    # Use asyncio.gather to run both functions concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(age_threshold=40)
    )

    print("\n--- Concurrent Fetch Results ---")
    print("All Users:")
    for user in all_users:
        print(user)

    print(f"\nUsers Older Than 40:")
    for user in older_users:
        print(user)

# --- Main Execution ---
if __name__ == "__main__":
    # Ensure the database is set up before running async operations
    setup_database()

    # Run the concurrent fetch operation
    start_time = time.time()
    asyncio.run(fetch_concurrently())
    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")

