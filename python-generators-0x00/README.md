Python Database Seeding Script (seed.py)

This script (seed.py) is designed to set up and populate a MySQL database named ALX_prodev with sample user data. It's a foundational component for projects that require a pre-filled database for testing, development, or demonstrating data streaming with Python generators.

Purpose

The primary purpose of seed.py is to:

Connect to a MySQL server.

Create a dedicated database (ALX_prodev) if it doesn't exist.

Create a user_data table within this database.

Populate the user_data table with sample data from a CSV file, ensuring data uniqueness by generating UUIDs for user_id and preventing duplicate insertions on subsequent runs.

Database Schema

The ALX_prodev database will contain a table named user_data with the following structure:

Field

Type

Constraints

Description

user_id

VARCHAR(36)

PRIMARY KEY, UUID, INDEXED

Unique identifier for each user.

name

VARCHAR(255)

NOT NULL

The user's full name.

email

VARCHAR(255)

NOT NULL

The user's email address.

age

DECIMAL(3,0)

NOT NULL

The user's age.

Functions
The seed.py script provides the following functions:

connect_db():

Establishes a connection to the MySQL database server.

Reads connection details (host, user, password) from environment variables.

Returns a mysql.connector.connection object or None on failure.

create_database(connection):

Creates the ALX_prodev database if it does not already exist.

Requires an active connection to the MySQL server.

connect_to_prodev():

Establishes a connection specifically to the ALX_prodev database.

Reads connection details from environment variables.

Returns a mysql.connector.connection object or None on failure.

create_table(connection):

Creates the user_data table within the connected database if it does not already exist, adhering to the specified schema.

Requires an active connection to the ALX_prodev database.

insert_data(connection, csv_file_path):

Reads data from a specified CSV file (e.g., user_data.csv).

Generates a unique UUID for each user_id.

Inserts the data into the user_data table.

Important: It checks if the table is empty before inserting to prevent duplicate entries on successive runs.

Setup and Usage
To use this script, follow these steps:

Clone the repository (if applicable):

git clone https://github.com/alx-backend-python/python-generators-0x00.git
cd python-generators-0x00

Create a Virtual Environment (Recommended):

python3 -m venv venv
source venv/bin/activate

Install Dependencies:

The script relies on mysql-connector-python for database interaction and python-dotenv for environment variable management.

pip install mysql-connector-python python-dotenv

Create a .env file:

In the same directory as seed.py, create a file named .env and add your MySQL connection details:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_root_password # Replace with your MySQL root password
DB_NAME=ALX_prodev

Ensure your MySQL server is running.

Prepare user_data.csv:

Make sure you have a user_data.csv file in the same directory as seed.py with name, email, and age columns. An example user_data.csv content is:

name,email,age
Dan Altenwerth Jr.,Molly59@gmail.com,67
Glenda Wisozk,Miriam21@gmail.com,119
Daniel Fahey IV,Delia.Lesch11@hotmail.com,49
Ronnie Bechtelar,Sandra19@yahoo.com,22
Alma Bechtelar,Shelly_Balistreri22@hotmail.com,102

Run the Main Script:

The 0-main.py script (as provided in the prompt) orchestrates the execution of the functions in seed.py.

./0-main.py

This will connect to the database, create the ALX_prodev database and user_data table (if they don't exist), insert the data from user_data.csv, and then print a confirmation and the first 5 rows of the user_data table.

Example Output

connection successful

Successfully connected to database 'ALX_prodev'

Table 'user_data' created successfully (or already exists).

Table 'user_data' is empty. Inserting data from 'user_data.csv'...

Successfully inserted 5 rows into 'user_data'.

Database ALX_prodev is present
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119), ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49), ('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22), ('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly_Balistreri22@hotmail.com', 102)]
