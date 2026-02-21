import sqlite3
from werkzeug.security import generate_password_hash

username = "Admin"
password = "Admin@2026"

hashed_password = generate_password_hash(password)

conn = sqlite3.connect("complaints.db")
c = conn.cursor()

# Create users table if not exists
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
''')

# Insert or update admin user
c.execute("INSERT OR REPLACE INTO users (username, password) VALUES (?, ?)",
          (username, hashed_password))

conn.commit()
conn.close()

print("✅ Admin user created successfully!")