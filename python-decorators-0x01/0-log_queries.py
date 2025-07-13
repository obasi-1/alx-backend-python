import sqlite3
import functools
import os

def setup_dummy_database():
    """Sets up a simple in-memory SQLite database for demonstration."""
    # Remove the database file if it exists to ensure a clean start
    if os.path.exists('users.db'):
        os.remove('users.db')
        
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Create a users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    # Insert some sample data
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Alice', 'alice@example.com'))
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Bob', 'bob@example.com'))
    conn.commit()
    conn.close()

def log_queries(func):
    """
    A decorator that logs the SQL query string of a function before executing it.
    It assumes the query is passed as the first positional argument or a keyword argument named 'query'.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Attempt to find the query string in the function's arguments
        query_str = ""
        if 'query' in kwargs:
            query_str = kwargs['query']
        elif args:
            # Assuming the query is the first positional argument
            query_str = args[0]

        # Log the query if it was found
        if query_str:
            print(f"[LOG] Executing Query: \"{query_str}\"")
        else:
            print("[LOG] Decorator could not find the query string to log.")
        
        # Execute the original function and return its result
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Connects to the database, executes a given query, and fetches all results.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Main execution block
if __name__ == "__main__":
    print("--- Setting up the database ---")
    setup_dummy_database()
    print("Database 'users.db' created with sample data.\n")

    print("--- Fetching users while logging the query ---")
    # The @log_queries decorator will intercept this call
    users = fetch_all_users(query="SELECT * FROM users")

    print("\n--- Query Results ---")
    if users:
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    else:
        print("No users found.")

    # Clean up the created database file
    if os.path.exists('users.db'):
        os.remove('users.db')
    print("\n--- Cleaned up database file ---")
