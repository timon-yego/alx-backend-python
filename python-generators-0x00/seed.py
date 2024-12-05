import mysql.connector
import csv
import uuid

# Function to connect to the MySQL database server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="Mydatabase@99#"  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the ALX_prodev database if it doesn't exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created successfully (or already exists).")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to connect to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="Mydatabase@99#",  
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the user_data table if it doesn't exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3, 0) NOT NULL,
                INDEX (user_id)
            );
        """)
        print("Table user_data created successfully.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to insert data into the user_data table
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        # Read data from the CSV file
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                user_id = str(uuid.uuid4())  # Generate a unique UUID
                name, email, age = row
                # Insert data only if it doesn't exist
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (user_id, name, email, int(age)))
        connection.commit()
        print("Data inserted successfully.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found.")

# Generator to stream rows from the SQL database one by one
def stream_data(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
