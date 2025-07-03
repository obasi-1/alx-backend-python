# 4-stream_ages.py
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

def stream_user_ages():
    """
    A generator function that streams user ages one by one from the
    'user_data' table in the ALX_prodev MySQL database.

    This function uses exactly one loop to fetch data.

    Yields:
        int: The age of a user.
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor() # Default cursor returns tuples
            
            # Select only the age column for efficiency
            cursor.execute("SELECT age FROM user_data")
            
            # Loop 1: Fetch rows one by one
            row = cursor.fetchone()
            while row:
                yield row[0] # Yield the age (first element of the tuple)
                row = cursor.fetchone()
        else:
            print("Failed to connect to the database. Cannot stream user ages.")
            return # Exit generator if connection failed

    except mysql.connector.Error as err:
        print(f"Database error during age streaming: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during age streaming: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def calculate_average_age():
    """
    Calculates the average age of users without loading the entire dataset
    into memory, using the stream_user_ages generator.

    This function uses one loop (iterating over the generator),
    making the total loops in the script two (one in stream_user_ages, one here).

    Returns:
        float: The average age of users. Returns 0.0 if no users are found.
    """
    total_age = 0
    user_count = 0

    # Loop 2: Iterate over ages yielded by the generator
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    if user_count == 0:
        return 0.0 # Avoid division by zero if no users are found
    
    return total_age / user_count

if __name__ == '__main__':
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")
