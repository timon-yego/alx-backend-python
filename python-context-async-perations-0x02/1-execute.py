import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        # Open the database connection
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the database connection
        if self.connection:
            self.connection.close()
        # Handle exceptions if any
        if exc_type:
            print(f"An error occurred: {exc_val}")
        return False  # Re-raise the exception if any

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.result = None

    def __enter__(self):
        # Open the database connection
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the database connection
        if self.connection:
            self.connection.close()
        # Handle exceptions if any
        if exc_type:
            print(f"An error occurred: {exc_val}")
        return False  # Re-raise the exception if any

# Create a test database and a table for demonstration
with sqlite3.connect("example.db") as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?), (?, ?)", ("Alice", 30, "Bob", 20))
    conn.commit()

# Use the custom context manager to execute a query
query = "SELECT * FROM users WHERE age > ?"
param = (25,)
with ExecuteQuery("example.db", query, param) as results:
    for row in results:
        print(row)
