import time
import sqlite3
import functools

# Global cache for query results
query_cache = {}

# --- Copied from previous task: with_db_connection decorator ---
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

# --- New: cache_query decorator ---
def cache_query(func):
    """
    A decorator that caches the results of a database query.
    It assumes the SQL query string is passed as a keyword argument named 'query'
    or as the second positional argument (after 'conn').
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs): # Expects 'conn' as the first argument
        # Determine the query string from args or kwargs
        query = None
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 0: # Check if there's a second positional argument for the query
            query = args[0] # Assuming query is the first *additional* arg after conn

        if query is None:
            print("Warning: No 'query' argument found for caching. Executing without caching.")
            return func(conn, *args, **kwargs)

        if query in query_cache:
            print(f"Cache hit for query: '{query}' - returning cached result.")
            return query_cache[query]
        else:
            print(f"Cache miss for query: '{query}' - executing query.")
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            print(f"Query result cached for: '{query}'.")
            return result
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
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetches users from the database based on the given query.
    This function's results will be cached.
    """
    print(f"Executing actual database query: {query}")
    cursor = conn.cursor()
    cursor.execute(query)
    # Simulate some work to make caching noticeable
    time.sleep(0.5)
    return cursor.fetchall()

# First call will execute the query and cache the result
print("\n--- First call: Fetching all users ---")
users = fetch_users_with_cache(query="SELECT * FROM users")
print("Users from first call:", users)

# Second call with the same query will use the cached result
print("\n--- Second call: Fetching all users again (should be cached) ---")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Users from second call:", users_again)

# Third call with a different query will execute and cache a new result
print("\n--- Third call: Fetching user with ID 1 (new query) ---")
user_id_1 = fetch_users_with_cache(query="SELECT * FROM users WHERE id = 1")
print("User with ID 1:", user_id_1)

# Fourth call with the same new query will use the cached result
print("\n--- Fourth call: Fetching user with ID 1 again (should be cached) ---")
user_id_1_again = fetch_users_with_cache(query="SELECT * FROM users WHERE id = 1")
print("User with ID 1 again:", user_id_1_again)

# Clear the cache for demonstration purposes
print("\n--- Clearing cache and re-fetching ---")
query_cache.clear()
print("Cache cleared.")

print("\n--- Fifth call: Fetching all users after cache clear (should execute again) ---")
users_after_clear = fetch_users_with_cache(query="SELECT * FROM users")
print("Users after cache clear:", users_after_clear)
