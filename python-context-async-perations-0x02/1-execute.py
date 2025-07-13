import sqlite3

class ExecuteQuery:
    """
    A class-based context manager for executing a specific database query
    and automatically managing the connection, execution, and result retrieval.
    It handles committing changes on success and rolling back on error.
    """
    def __init__(self, db_name='users.db', query=None, params=None):
        """
        Initializes the ExecuteQuery context manager with the database name,
        the SQL query to execute, and its parameters.

        Args:
            db_name (str): The name of the SQLite database file.
            query (str): The SQL query string to execute.
            params (tuple or list, optional): Parameters for the SQL query. Defaults to None.
        """
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.results = None

    def __enter__(self):
        """
        Enters the runtime context. Opens the database connection,
        executes the query, and stores the results.

        Returns:
            list: The fetched results from the executed query.
        """
        if not self.query:
            raise ValueError("A SQL query must be provided to ExecuteQuery.")

        try:
            self.conn = sqlite3.connect(self.db_name)
            cursor = self.conn.cursor()
            print(f"Database connection to '{self.db_name}' opened for query.")
            print(f"Executing query: '{self.query}' with params: {self.params}")

            cursor.execute(self.query, self.params)
            self.results = cursor.fetchall() # Store results for return

            return self.results
        except sqlite3.Error as e:
            print(f"Error during query execution: {e}")
            if self.conn:
                self.conn.rollback() # Rollback on error
                print("Transaction rolled back due to error.")
            raise # Re-raise the exception

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the runtime context. Handles committing or rolling back
        the transaction based on whether an exception occurred, and closes
        the database connection.
        """
        if self.conn:
            if exc_type:
                # An exception occurred inside the 'with' block
                print(f"An exception of type {exc_type.__name__} occurred: {exc_val}. Rolling back changes.")
                self.conn.rollback()
            else:
                # No exception, commit changes
                print("No exception occurred. Committing changes if any.")
                self.conn.commit()
            self.conn.close()
            print(f"Database connection to '{self.db_name}' closed after query.")
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
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    ''')
    # Insert some dummy data if the table is empty, including age
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (1, 'Alice Smith', 'alice@example.com', 30)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (2, 'Bob Johnson', 'bob@example.com', 22)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (3, 'Charlie Brown', 'charlie@example.com', 35)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (4, 'Diana Prince', 'diana@example.com', 28)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (5, 'Eve Adams', 'eve@example.com', 20)")
    conn.commit()
    conn.close()
    print("Database 'users.db' and table 'users' ensured to exist with dummy data (including age).")

# Set up the database before using the context manager
setup_database()

print("\n--- Using ExecuteQuery context manager to fetch users older than 25 ---")
try:
    query_str = "SELECT * FROM users WHERE age > ?"
    param_val = 25
    with ExecuteQuery(query=query_str, params=(param_val,)) as users_over_25:
        print(f"Users older than {param_val}:")
        for user in users_over_25:
            print(user)
except Exception as e:
    print(f"An error occurred: {e}")

print("\n--- Using ExecuteQuery context manager to fetch all users ---")
try:
    with ExecuteQuery(query="SELECT * FROM users") as all_users:
        print("All Users:")
        for user in all_users:
            print(user)
except Exception as e:
    print(f"An error occurred: {e}")

print("\n--- Using ExecuteQuery context manager to update an email (and commit) ---")
try:
    update_query_str = "UPDATE users SET email = ? WHERE id = ?"
    update_params = ("charlie.new@example.com", 3)
    with ExecuteQuery(query=update_query_str, params=update_params) as result:
        print(f"Update operation completed. Result: {result}") # result will be empty for UPDATE
except Exception as e:
    print(f"An error occurred during update: {e}")

# Verify the update
print("\n--- Verifying updated email for Charlie Brown ---")
try:
    with ExecuteQuery(query="SELECT email FROM users WHERE id = ?", params=(3,)) as email_result:
        print(f"Email for user ID 3: {email_result[0][0] if email_result else 'Not Found'}")
except Exception as e:
    print(f"An error occurred during verification: {e}")


print("\n--- Using ExecuteQuery context manager with a simulated error (should rollback) ---")
try:
    # First, get original email for user ID 4 to verify rollback
    original_email_4 = None
    with ExecuteQuery(query="SELECT email FROM users WHERE id = ?", params=(4,)) as email_res:
        original_email_4 = email_res[0][0] if email_res else None
    print(f"Original email for user ID 4: {original_email_4}")

    # Attempt to update with a simulated error
    faulty_query = "UPDATE users SET email = ? WHERE id = ?"
    faulty_params = ("faulty.diana@example.com", 4)
    with ExecuteQuery(query=faulty_query, params=faulty_params) as result:
        print("Simulating an error after execution...")
        raise ValueError("Simulated error after query execution!") # This will trigger rollback
except ValueError as e:
    print(f"Caught expected error: {e}. Transaction should have rolled back.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Verify the rollback
print("\n--- Verifying email for user ID 4 after simulated rollback ---")
try:
    with ExecuteQuery(query="SELECT email FROM users WHERE id = ?", params=(4,)) as email_after_rollback:
        print(f"Email for user ID 4 after rollback attempt: {email_after_rollback[0][0] if email_after_rollback else 'Not Found'}")
        if original_email_4 and email_after_rollback and email_after_rollback[0][0] == original_email_4:
            print("Rollback successful: Email remained unchanged.")
        else:
            print("Rollback failed or email changed unexpectedly.")
except Exception as e:
    print(f"An error occurred during verification after rollback: {e}")
