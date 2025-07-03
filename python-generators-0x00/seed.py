# seed.py
import mysql.connector
import os
from dotenv import load_dotenv
import csv
import uuid

# Load environment variables from .env file
load_dotenv()

def connect_db():
    """
    Connects to the MySQL database server using credentials from environment variables.
    Returns the connection object if successful, None otherwise.
    """
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '') # Empty string for no password
    
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        print(f"Successfully connected to MySQL server at {db_host}")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    """
    Creates the database ALX_prodev if it does not already exist.
    Requires a connection to the MySQL server (not a specific database).
    """
    if not connection:
        print("No database connection provided to create_database.")
        return

    db_name = os.getenv('DB_NAME', 'ALX_prodev')
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' ensured to exist.")
    except mysql.connector.Error as err:
        print(f"Error creating database '{db_name}': {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL using credentials from environment variables.
    Returns the connection object if successful, None otherwise.
    """
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'ALX_prodev')

    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        print(f"Successfully connected to database '{db_name}'")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database '{db_name}': {err}")
        return None

def create_table(connection):
    """
    Creates the 'user_data' table if it does not already exist with the required fields.
    Requires a connection to the 'ALX_prodev' database.
    """
    if not connection:
        print("No database connection provided to create_table.")
        return

    cursor = connection.cursor()
    table_name = "user_data"
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        INDEX idx_user_id (user_id) -- Primary key automatically creates an index, but explicitly showing for clarity.
    );
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{table_name}' created successfully (or already exists).")
    except mysql.connector.Error as err:
        print(f"Error creating table '{table_name}': {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_file_path):
    """
    Inserts data from the specified CSV file into the 'user_data' table.
    Data is inserted only if the table is empty to prevent duplicate entries on re-run.
    Generates a UUID for each user_id.
    """
    if not connection:
        print("No database connection provided to insert_data.")
        return

    cursor = connection.cursor()
    table_name = "user_data"

    try:
        # Check if the table is empty
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        if cursor.fetchone()[0] > 0:
            print(f"Table '{table_name}' is not empty. Skipping data insertion.")
            return

        print(f"Table '{table_name}' is empty. Inserting data from '{csv_file_path}'...")
        
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader) # Skip header row

            data_to_insert = []
            for row in reader:
                try:
                    # Generate a UUID for user_id
                    user_id = str(uuid.uuid4())
                    name = row[0]
                    email = row[1]
                    age = int(row[2]) # Convert age to integer as per DECIMAL(3,0)
                    data_to_insert.append((user_id, name, email, age))
                except (ValueError, IndexError) as e:
                    print(f"Skipping malformed row: {row} - Error: {e}")
                    continue

            if data_to_insert:
                insert_query = f"""
                INSERT INTO {table_name} (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
                """
                cursor.executemany(insert_query, data_to_insert)
                connection.commit()
                print(f"Successfully inserted {len(data_to_insert)} rows into '{table_name}'.")
            else:
                print("No valid data found in CSV to insert.")

    except mysql.connector.Error as err:
        print(f"Error inserting data into '{table_name}': {err}")
        connection.rollback() # Rollback changes on error
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        cursor.close()

if __name__ == '__main__':
    # This block is for testing the functions directly if seed.py is run.
    # The 0-main.py script handles the execution flow as per the prompt.
    print("This script provides functions for database seeding. Run 0-main.py to execute the full flow.")
    print("Ensure you have a .env file with DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME.")
    print("Make sure 'mysqlclient' and 'python-dotenv' are installed: pip install mysqlclient python-dotenv")
