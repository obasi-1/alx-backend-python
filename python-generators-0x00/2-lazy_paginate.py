# 2-lazy_paginate.py
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

def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the 'user_data' table
    in the ALX_prodev MySQL database.

    Args:
        page_size (int): The maximum number of rows to fetch for this page.
        offset (int): The starting point (offset) for fetching rows.

    Returns:
        list[dict]: A list of user dictionaries for the current page.
                    Returns an empty list if no more rows are found.
    """
    connection = None
    cursor = None
    rows = []
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            # Fetch all columns using SELECT * and apply LIMIT and OFFSET for pagination
            # Ordering is added to ensure consistent pagination results.
            cursor.execute(f"SELECT * FROM user_data ORDER BY user_id LIMIT {page_size} OFFSET {offset}")
            rows = cursor.fetchall()
        else:
            print("Failed to connect to the database. Cannot paginate users.")
    except mysql.connector.Error as err:
        print(f"Database error during pagination: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during pagination: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return rows

def lazy_pagination(page_size):
    """
    A generator function that lazily loads pages of user data from the
    'user_data' table. It fetches the next page only when needed,
    starting from an offset of 0.

    This function uses exactly one loop.

    Args:
        page_size (int): The number of users to fetch per page.

    Yields:
        list[dict]: A list of user dictionaries representing a page of data.
                    The generator stops when an empty page is returned.
    """
    offset = 0
    # Loop 1: Continuously fetch pages until no more data is available
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break  # No more data, exit the generator
        yield page # Yield the current page (a list of user dictionaries)
        offset += page_size # Increment offset for the next page
