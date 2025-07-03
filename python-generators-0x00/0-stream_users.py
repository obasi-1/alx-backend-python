# 0-stream_users.py
import mysql.connector
import os
import sys

# Add the directory containing seed.py to the Python path
# This allows importing seed.py directly if it's in the same directory
# or a known path. Adjust if seed.py is in a different location.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the seed module functions
# Ensure seed.py is accessible in the Python path or current directory
try:
    import seed
except ImportError:
    print("Error: 'seed.py' not found. Make sure it's in the same directory or accessible via PYTHONPATH.")
    sys.exit(1)

def stream_users():
    """
    A generator function that streams rows from the 'user_data' table
    in the ALX_prodev MySQL database one by one.
    Each row is yielded as a dictionary.
    This function uses the 'yield' keyword to implement the generator.
    It contains no more than 1 explicit loop.
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if connection:
            # Use dictionary=True to fetch rows as dictionaries
            cursor = connection.cursor(dictionary=True)
            
            # Select all user data
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # Fetch rows one by one using a single loop
            row = cursor.fetchone()
            while row:
                yield row # Yield the current row (as a dictionary)
                row = cursor.fetchone() # Fetch the next row
        else:
            print("Failed to connect to the database. Cannot stream users.")
            return # Exit generator if connection failed

    except mysql.connector.Error as err:
        print(f"Database error during streaming: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during streaming: {e}")
    finally:
        # Ensure cursor and connection are closed even if errors occur
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        # print("Database connection closed.") # Optional: for debugging connection closure
