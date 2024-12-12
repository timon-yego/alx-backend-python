import sqlite3
import aiosqlite
import asyncio

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

async def async_fetch_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:")
    for row in results[0]:
        print(row)

    print("Users older than 40:")
    for row in results[1]:
        print(row)

# Create a test database and a table for demonstration
async def setup_database():
    async with aiosqlite.connect("example.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [("Alice", 30), ("Bob", 20), ("Charlie", 45), ("Diana", 50)]
        )
        await db.commit()

# Run the setup and fetch concurrently
async def main():
    await setup_database()
    await fetch_concurrently()

if __name__ == "__main__":
    asyncio.run(main())
