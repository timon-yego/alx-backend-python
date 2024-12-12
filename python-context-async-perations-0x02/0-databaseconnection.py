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

# Create a test database and a table for demonstration
with sqlite3.connect("example.db") as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES (?), (?)", ("Alice", "Bob"))
    conn.commit()

# Use the custom context manager to perform a query
with DatabaseConnection("example.db") as db:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)
