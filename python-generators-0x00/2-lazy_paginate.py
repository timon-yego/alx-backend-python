import seed

def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator function to fetch paginated data lazily.
    Fetches users in pages of the given page size starting at offset 0.

    Args:
        page_size (int): The number of records to fetch per page.

    Yields:
        list: A batch of users fetched from the database.
    """
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)  # Fetch the next page
        if not rows:  # If no rows are returned, stop iteration
            break
        yield rows  # Yield the current batch of users
        offset += page_size  # Increment offset for the next page