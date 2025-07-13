import time
import sqlite3
import functools

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

# --- New: retry_on_failure decorator ---
def retry_on_failure(retries=3, delay=2):
    """
    A decorator factory that retries the decorated function a specified number of times
    if it raises an exception.

    Args:
        retries (int): The maximum number of times to retry the function.
        delay (int): The delay in seconds between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries + 1): # +1 to include the initial attempt
                try:
                    print(f"Attempt {i + 1}/{retries + 1} for function '{func.__name__}'...")
                    return func(*args, **kwargs)
                except Exception as e:
                    if i < retries:
                        print(f"Attempt {i + 1} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries + 1} attempts failed. Last error: {e}")
                        raise # Re-raise the last exception if all retries are exhausted
        return wrapper
    return decorator

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

# Global counter to simulate transient failures
failure_count = 0
MAX_FAILURES = 2 # Simulate failure for the first 2 calls

@with_db_connection
@retry_on_failure(retries=3, delay=1) # Retry up to 3 times with 1 second delay
def fetch_users_with_retry(conn):
    """
    Fetches all users from the database.
    Simulates a transient error for the first few calls.
    """
    global failure_count
    if failure_count < MAX_FAILURES:
        failure_count += 1
        print(f"Simulating a transient database error (failure {failure_count}/{MAX_FAILURES})...")
        raise sqlite3.OperationalError("Database is temporarily unavailable.")
    print("Successfully connected and fetching users.")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
print("\n--- Attempting to fetch users with retry logic ---")
try:
    users = fetch_users_with_retry()
    print("Fetched Users:", users)
except Exception as e:
    print(f"Failed to fetch users after multiple retries: {e}")

# Reset failure count for another test
failure_count = 0
print("\n--- Attempting to fetch users again (should succeed after retries) ---")
try:
    users_again = fetch_users_with_retry()
    print("Fetched Users Again:", users_again)
except Exception as e:
    print(f"Failed to fetch users again after multiple retries: {e}")

# Test case that will always fail (retries exhausted)
failure_count = 0 # Reset for this test
MAX_FAILURES = 5 # Set failures higher than retries
print("\n--- Attempting to fetch users with too many failures (should ultimately fail) ---")
try:
    users_fail = fetch_users_with_retry()
    print("Fetched Users (unexpected success):", users_fail)
except Exception as e:
    print(f"Successfully failed to fetch users after exhausting retries: {e}")

