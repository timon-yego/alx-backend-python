import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
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

def stream_users():
    """
    Generator function to stream rows from the user_data table.
    Yields each row as a dictionary.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True,  buffered=True)
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
