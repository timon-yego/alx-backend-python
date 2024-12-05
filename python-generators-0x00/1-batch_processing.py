import mysql.connector

def connect_to_prodev():
    """
    Connect to the ALX_prodev database.
    """
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


def stream_users_in_batches(batch_size):
    """
    Generator to fetch rows in batches from the user_data table.
    :param batch_size: The number of rows to fetch in each batch.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True)
        offset = 0

        while True:
            cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
            batch = cursor.fetchall()
            if not batch:  # Stop if no more rows are returned
                break
            yield batch
            offset += batch_size
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Process batches of users and filter those over the age of 25.
    :param batch_size: The number of rows to fetch in each batch.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user["age"] > 25]
        yield filtered_users


