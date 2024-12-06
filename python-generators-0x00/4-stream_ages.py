import seed

def stream_user_ages():
    """
    Generator function that streams user ages one by one.

    Yields:
        int: The age of a user.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    cursor.close()
    connection.close()

def calculate_average_age():
    """
    Calculates the average age of users using the stream_user_ages generator.

    Prints:
        Average age of users: <average age>
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found.")
