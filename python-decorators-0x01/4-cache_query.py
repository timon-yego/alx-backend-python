import time
import sqlite3 
import functools

# Dictionary to cache the results of SQL queries
query_cache = {}

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

def cache_query(func):
    """
    Caches the results of SQL queries to avoid redundant database calls.
    The cache is based on the query string.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Check if the query result is already cached
        if query in query_cache:
            print("Returning cached result for query:", query)
            return query_cache[query]
        
        # If not cached, execute the query and store the result
        print("Executing query:", query)
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result  # Cache the result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print("First call results:", users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Second call results:", users_again)
