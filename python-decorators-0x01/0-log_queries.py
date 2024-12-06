import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries
def log_queries():
    """
    Decorator to log SQL queries executed by the decorated function.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Log the SQL query
            query = kwargs.get('query') if 'query' in kwargs else args[0]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Executing SQL query: {query}")
            # Execute the original function
            return func(*args, **kwargs)
        return wrapper
    return decorator


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")