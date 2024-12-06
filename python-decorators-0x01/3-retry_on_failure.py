import time
import sqlite3 
import functools

def with_db_connection(func):
    """
    Decorator to handle opening and closing of database connections.
    Passes the database connection to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument to the function
            return func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is closed after the function execution
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry the function execution in case of exceptions.
    Retries the function `retries` times with a `delay` in seconds between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    # Try executing the function
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    attempt += 1
                    print(f"Attempt {attempt}/{retries} failed: {e}")
                    if attempt < retries:
                        time.sleep(delay)  # Wait before retrying
                    else:
                        raise  # Raise the exception if all retries fail
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)