import sqlite3

class DatabaseConnection:
    """
    A class-based context manager for handling SQLite database connections.
    It automatically opens a connection upon entering the 'with' block
    and closes it upon exiting, ensuring proper resource management.
    """
    def __init__(self, db_name='users.db'):
        """
        Initializes the DatabaseConnection context manager.

        Args:
            db_name (str): The name of the SQLite database file.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Enters the runtime context related to this object.
        Opens the database connection and creates a cursor.

        Returns:
            sqlite3.Connection: The database connection object.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Database connection to '{self.db_name}' opened via context manager.")
            return self.conn
        except sqlite3.Error as e:
            print(f"Error opening database connection: {e}")
            # Re-raise the exception to indicate failure to enter the context
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the runtime context related to this object.
        Closes the database connection.

        Args:
            exc_type (type): The type of the exception that caused the context to be exited.
            exc_val (Exception): The exception instance.
            exc_tb (traceback): A traceback object encapsulating the call stack.
        """
        if self.conn:
            if exc_type:
                # An exception occurred inside the 'with' block
                print(f"An exception occurred: {exc_val}. Rolling back changes.")
                self.conn.rollback() # Rollback if an error occurred
            else:
                # No exception, commit changes
                print("No exception occurred. Committing changes.")
                self.conn.commit() # Commit changes if no error
            self.conn.close()
            print(f"Database connection to '{self.db_name}' closed via context manager.")
        # Return False to propagate the exception, or True to suppress it
        return False

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

# Set up the database before using the context manager
setup_database()

print("\n--- Using DatabaseConnection context manager to fetch users ---")
try:
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM users"
        print(f"Executing query: {query}")
        cursor.execute(query)
        results = cursor.fetchall()
        print("Query Results:", results)
except Exception as e:
    print(f"An error occurred during database operation: {e}")

print("\n--- Using DatabaseConnection context manager to update and commit ---")
try:
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        user_id_to_update = 1
        new_email = "alice.smith.new@example.com"
        update_query = "UPDATE users SET email = ? WHERE id = ?"
        print(f"Updating user ID {user_id_to_update} email to {new_email}")
        cursor.execute(update_query, (new_email, user_id_to_update))
        # No explicit commit needed here, __exit__ will handle it
except Exception as e:
    print(f"An error occurred during update operation: {e}")

# Verify the update
print("\n--- Verifying the updated email ---")
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (1,))
    updated_email = cursor.fetchone()
    print(f"Email for user ID 1 after update: {updated_email[0] if updated_email else 'Not Found'}")


print("\n--- Using DatabaseConnection context manager to update and rollback (simulated error) ---")
try:
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        user_id_to_update_rollback = 2
        original_email_2 = None
        # First, get original email to verify rollback
        cursor.execute("SELECT email FROM users WHERE id = ?", (user_id_to_update_rollback,))
        original_email_2 = cursor.fetchone()[0]
        print(f"Original email for user ID {user_id_to_update_rollback}: {original_email_2}")

        new_email_rollback = "bob.rollback@example.com"
        update_query_rollback = "UPDATE users SET email = ? WHERE id = ?"
        print(f"Attempting to update user ID {user_id_to_update_rollback} email to {new_email_rollback}")
        cursor.execute(update_query_rollback, (new_email_rollback, user_id_to_update_rollback))

        print("Simulating an error to trigger rollback...")
        raise ValueError("Simulated error during transaction!") # This will cause a rollback

except ValueError as e:
    print(f"Caught expected error: {e}. Transaction should have rolled back.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Verify the rollback
print("\n--- Verifying the email after simulated rollback ---")
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (2,))
    email_after_rollback = cursor.fetchone()
    print(f"Email for user ID 2 after rollback attempt: {email_after_rollback[0] if email_after_rollback else 'Not Found'}")
    # Assert that the email is still the original one
    # Note: original_email_2 is captured outside the try block for comparison
    print(f"Original email for comparison: {original_email_2}")
    if original_email_2 and email_after_rollback and email_after_rollback[0] == original_email_2:
        print("Rollback successful: Email remained unchanged.")
    else:
        print("Rollback failed or email changed unexpectedly.")
