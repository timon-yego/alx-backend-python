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

def transactional(func):
    """
    Decorator to manage database transactions.
    Commits changes if no error occurs; otherwise, rolls back.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Execute the wrapped function
            result = func(conn, *args, **kwargs)
            # Commit the transaction if successful
            conn.commit()
            return result
        except Exception as e:
            # Rollback the transaction in case of an error
            conn.rollback()
            raise e  # Re-raise the exception for debugging
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')