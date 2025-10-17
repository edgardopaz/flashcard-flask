import sqlite3
import os

# Print current directory and files
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

# Connect to the database
connection = sqlite3.connect('database.db')

# Initialize schema
with open('schema.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

# Insert sample posts
cur = connection.cursor()
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post'))
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post'))

# Save and close
connection.commit()
connection.close()

print("✅ Database initialized with schema and sample posts.")
