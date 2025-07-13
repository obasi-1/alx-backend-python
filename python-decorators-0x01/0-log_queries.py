import sqlite3
import functools
from datetime import datetime # Added import for datetime

# Define the decorator to log SQL queries
def log_queries(func):
    """
    A decorator that logs the SQL query before executing the decorated function.
    It assumes the SQL query is the first argument passed to the decorated function.
    The log message now includes a timestamp.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Get current timestamp
        # Check if there's at least one argument, which is expected to be the query
        if args:
            query = args[0] # Assuming the SQL query is the first positional argument
            print(f"[{timestamp}] Executing SQL Query: {query}") # Added timestamp to log
        else:
            print(f"[{timestamp}] Executing a database function, but no query argument found.") # Added timestamp to log

        # Call the original function with its arguments
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Connects to 'users.db', executes the given query, and fetches all results.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# --- Example Usage ---

# First, let's create a dummy 'users.db' and a 'users' table for demonstration
# This part is not part of the decorator, but necessary to run the example
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
    conn.commit()
    conn.close()
    print("Database 'users.db' and table 'users' ensured to exist with dummy data.")

# Set up the database before fetching
setup_database()

# Fetch users while logging the query
print("\n--- Fetching all users ---")
users = fetch_all_users(query="SELECT * FROM users")
print("Fetched Users:", users)

print("\n--- Fetching a specific user ---")
specific_user = fetch_all_users(query="SELECT * FROM users WHERE name = 'Alice Smith'")
print("Fetched Specific User:", specific_user)

print("\n--- Fetching with a non-existent query (still logs) ---")
no_users = fetch_all_users(query="SELECT * FROM users WHERE id = 999")
print("Fetched No Users:", no_users)
