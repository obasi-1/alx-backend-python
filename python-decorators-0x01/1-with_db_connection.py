import sqlite3
import functools

def with_db_connection(func):
    """
    A decorator that automatically opens a SQLite database connection ('users.db'),
    passes it as the first argument to the decorated function, and ensures
    the connection is closed after the function's execution, even if errors occur.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None # Initialize conn to None
        try:
            # Establish a connection to the database
            conn = sqlite3.connect('users.db')
            print("Database connection opened.")

            # Pass the connection object as the first argument to the decorated function
            # The original function signature expects 'conn' as its first parameter
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
            raise # Re-raise the exception after logging
        finally:
            # Ensure the connection is closed, regardless of success or failure
            if conn:
                conn.close()
                print("Database connection closed.")

    return wrapper

# --- Example Usage ---

# First, let's ensure 'users.db' and a 'users' table exist for demonstration
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    # Insert some dummy data if the table is empty
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice Smith', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob Johnson', 'bob@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (3, 'Charlie Brown', 'charlie@example.com')")
    conn.commit()
    conn.close()
    print("Database 'users.db' and table 'users' ensured to exist with dummy data.")

# Set up the database before defining and using the decorated function
setup_database()

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user from the 'users' table by their ID using the provided connection.
    """
    print(f"Executing get_user_by_id for user_id: {user_id}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
print("\n--- Fetching user with ID 1 ---")
user = get_user_by_id(user_id=1)
print("Fetched User:", user)

print("\n--- Fetching user with ID 2 ---")
user2 = get_user_by_id(user_id=2)
print("Fetched User:", user2)

print("\n--- Attempting to fetch non-existent user with ID 99 ---")
user_none = get_user_by_id(user_id=99)
print("Fetched User (non-existent):", user_none)
