# 1-batch_processing.py
import mysql.connector
import os
import sys

# Add the directory containing seed.py to the Python path
# This ensures seed.py can be imported if it's in the same directory
# or a known path. Adjust if seed.py is located elsewhere.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the seed module functions
try:
    import seed
except ImportError:
    print("Error: 'seed.py' not found. Make sure it's in the same directory or accessible via PYTHONPATH.")
    sys.exit(1)

def stream_users_in_batches(batch_size):
    """
    A generator function that fetches rows from the 'user_data' table
    in the ALX_prodev MySQL database in specified batch sizes.
    Each batch is yielded as a list of dictionaries.
    This function uses a single loop to fetch data efficiently.

    Args:
        batch_size (int): The number of rows to fetch in each batch.

    Yields:
        list[dict]: A list of user dictionaries for each batch.
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, name, email, age FROM user_data ORDER BY user_id") # Order for consistent batching
            
            # Loop 1: Fetch rows in batches
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break # No more rows to fetch
                yield batch
        else:
            print("Failed to connect to the database. Cannot stream users in batches.")
            return # Exit generator if connection failed

    except mysql.connector.Error as err:
        print(f"Database error during batch streaming: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during batch streaming: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def batch_processing(batch_size):
    """
    A generator function that processes user data in batches.
    It fetches batches using stream_users_in_batches and then filters
    users who are over the age of 25.
    This function uses the 'yield' keyword to stream filtered users one by one.
    It adheres to the constraint of having no more than 3 loops in total
    across both stream_users_in_batches and this function.

    Args:
        batch_size (int): The size of batches to fetch and process.

    Yields:
        dict: A dictionary representing a user who is over the age of 25.
    """
    # Loop 2: Iterate over batches yielded by stream_users_in_batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Iterate over each user within the current batch
        for user in batch:
            if user.get('age') is not None and user['age'] > 25:
                yield user

# Example usage (as per 2-main.py):
# if __name__ == '__main__':
#     import sys
#     print("Running batch_processing with batch_size=50. Outputting first 5 users over 25.")
#     try:
#         count = 0
#         for user in batch_processing(50):
#             print(user)
#             count += 1
#             if count >= 5: # Limit output for demonstration
#                 break
#     except BrokenPipeError:
#         # Handle cases where stdout pipe is closed (e.g., when piping to `head`)
#         sys.stderr.close()
