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

# --- New: transactional decorator ---
def transactional(func):
    """
    A decorator that manages database transactions. It assumes the decorated
    function receives a database connection object as its first argument.
    If the decorated function executes successfully, the transaction is committed.
    If an error occurs, the transaction is rolled back.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs): # Expects 'conn' as the first argument
        try:
            print("Transaction started.")
            result = func(conn, *args, **kwargs)
            conn.commit() # Commit changes if function executes successfully
            print("Transaction committed.")
            return result
        except Exception as e:
            conn.rollback() # Rollback changes if an error occurs
            print(f"Transaction rolled back due to error: {e}")
            raise # Re-raise the exception to propagate it

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

# Helper function to check user email (for verification)
@with_db_connection
def get_user_email(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates a user's email in the 'users' table.
    This function is wrapped by both with_db_connection and transactional.
    """
    print(f"Attempting to update user ID {user_id} email to {new_email}")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    # For demonstration, let's simulate an error for a specific user_id
    if user_id == 2:
        print("Simulating an error for user ID 2 to test rollback.")
        raise ValueError("Simulated error during update for user ID 2")

# --- Test Cases ---

# Test 1: Successful update
print("\n--- Test Case 1: Successful Email Update ---")
original_email_1 = get_user_email(user_id=1)
print(f"Original email for user ID 1: {original_email_1}")
try:
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    updated_email_1 = get_user_email(user_id=1)
    print(f"New email for user ID 1: {updated_email_1}")
    assert updated_email_1 == 'Crawford_Cartwright@hotmail.com'
    print("Test 1 Passed: Email updated and committed.")
except Exception as e:
    print(f"Test 1 Failed: An unexpected error occurred: {e}")


# Test 2: Update with simulated error (should rollback)
print("\n--- Test Case 2: Email Update with Simulated Error (Rollback) ---")
original_email_2 = get_user_email(user_id=2)
print(f"Original email for user ID 2: {original_email_2}")
try:
    update_user_email(user_id=2, new_email='error_test@example.com')
except ValueError as e:
    print(f"Caught expected error: {e}")
    updated_email_2 = get_user_email(user_id=2)
    print(f"Email for user ID 2 after rollback attempt: {updated_email_2}")
    assert updated_email_2 == original_email_2 # Email should remain unchanged
    print("Test 2 Passed: Email update rolled back successfully.")
except Exception as e:
    print(f"Test 2 Failed: An unexpected error occurred: {e}")

